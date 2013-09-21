from srcpy.module_generators import SemiSharedModuleGenerator
from srcpy.matchers import calldef_withtypes

from pyplusplus import function_transformers as FT
from pyplusplus.module_builder import call_policies
from pyplusplus import messages
from pygccxml.declarations import matcher, matchers, pointer_t, const_t, reference_t, declarated_t, char_t
from pyplusplus import code_creators

# Templates for client and server class
tmpl_clientclass = '''virtual ClientClass* GetClientClass() {
#if defined(_WIN32) // POSIX: TODO
        if( GetCurrentThreadId() != g_hPythonThreadID )
            return %(clsname)s::GetClientClass();
#endif // _WIN32
        ClientClass *pClientClass = SrcPySystem()->Get<ClientClass *>( "pyClientClass", GetPyInstance(), NULL, true );
        if( pClientClass )
            return pClientClass;
        return %(clsname)s::GetClientClass();
    }
'''

tmpl_serverclass = '''virtual ServerClass* GetServerClass() {
#if defined(_WIN32)
#if defined(_DEBUG)
        Assert( GetCurrentThreadId() == g_hPythonThreadID );
#elif defined(PY_CHECKTHREADID)
        if( GetCurrentThreadId() != g_hPythonThreadID )
            Error( "GetServerClass: Client? %%d. Thread ID is not the same as in which the python interpreter is initialized! %%d != %%d. Tell a developer.\\n", CBaseEntity::IsClient(), g_hPythonThreadID, GetCurrentThreadId() );
#endif // _DEBUG/PY_CHECKTHREADID
#endif // _WIN32
#if defined(_DEBUG) || defined(PY_CHECK_LOG_OVERRIDES)
        if( py_log_overrides.GetBool() )
            Msg("Calling GetServerClass(  ) of Class: %(clsname)s\\n");
#endif // _DEBUG/PY_CHECK_LOG_OVERRIDES
        ServerClass *pServerClass = SrcPySystem()->Get<ServerClass *>( "pyServerClass", GetPyInstance(), NULL, true );
        if( pServerClass )
            return pServerClass;
        return %(clsname)s::GetServerClass();
    }
'''

# Templates for entities handles and converters
tmpl_enthandle = '''{ //::%(handlename)s
        typedef bp::class_< %(handlename)s, bp::bases< CBaseHandle > > %(handlename)s_exposer_t;
        %(handlename)s_exposer_t %(handlename)s_exposer = %(handlename)s_exposer_t( "%(handlename)s", bp::init< >() );
        %(handlename)s_exposer.def( bp::init< %(clsname)s * >(( bp::arg("pVal") )) );
        %(handlename)s_exposer.def( bp::init< int, int >(( bp::arg("iEntry"), bp::arg("iSerialNumber") )) );
        { //::%(handlename)s::GetAttr
        
            typedef bp::object ( ::%(handlename)s::*GetAttr_function_type )( const char * ) const;
            
            %(handlename)s_exposer.def( 
                "__getattr__"
                , GetAttr_function_type( &::%(handlename)s::GetAttr )
            );
        
        }
        { //::%(handlename)s::Cmp
        
            typedef bool ( ::%(handlename)s::*Cmp_function_type )( bp::object ) const;
            
            %(handlename)s_exposer.def( 
                "__cmp__"
                , Cmp_function_type( &::%(handlename)s::Cmp )
            );
        
        }
        { //::%(handlename)s::NonZero
        
            typedef bool ( ::%(handlename)s::*NonZero_function_type )( ) const;
            
            %(handlename)s_exposer.def( 
                "__nonzero__"
                , NonZero_function_type( &::%(handlename)s::NonZero )
            );
        
        }
        { //::%(handlename)s::Set
        
            typedef void ( ::%(handlename)s::*Set_function_type )( %(clsname)s * ) const;
            
            %(handlename)s_exposer.def( 
                "Set"
                , Set_function_type( &::%(handlename)s::Set )
            );
        
        }
        { //::%(handlename)s::GetSerialNumber
        
            typedef int ( ::%(handlename)s::*GetSerialNumber_function_type )( ) const;
            
            %(handlename)s_exposer.def( 
                "GetSerialNumber"
                , GetSerialNumber_function_type( &::%(handlename)s::GetSerialNumber )
            );
        
        }
        { //::%(handlename)s::GetEntryIndex
        
            typedef int ( ::%(handlename)s::*GetEntryIndex_function_type )(  ) const;
            
            %(handlename)s_exposer.def( 
                "GetEntryIndex"
                , GetEntryIndex_function_type( &::%(handlename)s::GetEntryIndex )
            );
        
        }
        %(handlename)s_exposer.def( bp::self != bp::self );
        %(handlename)s_exposer.def( bp::self == bp::self );
    }
'''

tmpl_ent_converters = '''
struct %(ptr_convert_to_py_name)s : bp::to_python_converter<%(clsname)s *, ptr_%(clsname)s_to_handle>
{
    static PyObject* convert(%(clsname)s *s)
    {
        return s ? bp::incref(s->GetPyHandle().ptr()) : bp::incref(Py_None);
    }
};

struct %(convert_to_py_name)s : bp::to_python_converter<%(clsname)s, %(clsname)s_to_handle>
{
    static PyObject* convert(const %(clsname)s &s)
    {
        return bp::incref(s.GetPyHandle().ptr());
    }
};

struct %(convert_from_py_name)s
{
    handle_to_%(clsname)s()
    {
        bp::converter::registry::insert(
            &extract_%(clsname)s, 
            bp::type_id<%(clsname)s>()
            );
    }

    static void* extract_%(clsname)s(PyObject* op){
       CBaseHandle h = bp::extract<CBaseHandle>(op);
       if( h.Get() == NULL )
           return Py_None;
       return h.Get();
    }
};
'''

class Entities(SemiSharedModuleGenerator):
    module_name = '_entities'
    split = True
    
    # Includes
    files = [
        'cbase.h',
        'npcevent.h',
        'srcpy_entities.h',
        'bone_setup.h',
        'basegrenade_shared.h',
        '$takedamageinfo.h',
        '$c_ai_basenpc.h',
        '#SkyCamera.h',
        '#ai_basenpc.h',
        '#modelentities.h',
        '#basetoggle.h',
        '#triggers.h',
        '$soundinfo.h',
        '#nav_area.h',
        '#AI_Criteria.h',
        'saverestore.h',
        'vcollide_parse.h', # solid_t
        '#iservervehicle.h',
        '$iclientvehicle.h',
        '%choreoscene.h',
        '%choreoactor.h',
        '$steam/steamclientpublic.h', # CSteamID
        '$view_shared.h', # CViewSetup
        #'#%damagemodifier.h'
    ]
    
    # List of entity classes want to have exposed
    cliententities = [ 
        'C_BaseEntity', 
        'C_BaseAnimating',
        'C_BaseAnimatingOverlay',
        'C_BaseFlex',
        'C_BaseCombatCharacter',
        'C_BaseGrenade',
        'C_BasePlayer',
        'C_BaseCombatWeapon',
    ]

    serverentities = [ 
        'CBaseEntity', 
        'CBaseAnimating',
        'CBaseAnimatingOverlay',
        'CBaseFlex',
        'CBaseCombatCharacter',
        'CBaseGrenade',
        'CBasePlayer',
        'CBaseCombatWeapon',
        'CPointEntity',
        'CServerOnlyEntity',
        'CServerOnlyPointEntity',
        'CLogicalEntity',
        'CFuncBrush',
        'CBaseToggle',
        'CBaseTrigger',
    ]

    # Handle expose code
    def AddEntityConverter(self, mb, clsname):
        cls = mb.class_(clsname)
        
        handlename = '%sHANDLE' % (clsname)
        
        ptr_convert_to_py_name = 'ptr_%s_to_handle' % (clsname)
        convert_to_py_name = '%s_to_handle' % (clsname)
        convert_from_py_name = 'handle_to_%s' % (clsname)
        
        # Add handle typedef
        mb.add_declaration_code( 'typedef CEPyHandle< %s > %s;\r\n'% (clsname, handlename) )
        
        # Expose handle code
        mb.add_registration_code( tmpl_enthandle % {'clsname' : clsname, 'handlename' : handlename}, True )
        
        # Add declaration code for converters
        mb.add_declaration_code( tmpl_ent_converters % {
            'clsname' : clsname,
            'ptr_convert_to_py_name' : ptr_convert_to_py_name,
            'convert_to_py_name' : convert_to_py_name,
            'convert_from_py_name' : convert_from_py_name,
        })
        
        # Add registration code
        mb.add_registration_code( "%s();" % (ptr_convert_to_py_name) )
        mb.add_registration_code( "%s();" % (convert_to_py_name) )
        mb.add_registration_code( "%s();" % (convert_from_py_name) )
        
    # Parse methods
    def SetupEntityClass(self, mb, clsname):
        ''' This function is called for both exposed client and server entities and 
            applies shared functionality. '''
        cls = mb.class_(clsname)
        
        cls.include()
        cls.calldefs(matchers.access_type_matcher_t( 'protected' ), allow_empty=True).exclude()
        
        # Be selective about we need to override
        # DO NOT REMOVE. Some functions are not thread safe, which will cause runtime errors because we did not setup python threadsafe (slower)
        cls.mem_funs(allow_empty=True).virtuality = 'not virtual' 

        # Add converters + a python handle class
        self.AddEntityConverter(mb, clsname)  
        
        # Use by converters to check if a Python Object is attached
        cls.add_wrapper_code(
            'virtual PyObject *GetPySelf() const { return bp::detail::wrapper_base_::get_owner(*this); }'
        )
        
        # Test if the Entity class is setup right
        try:
            cls.mem_funs('CreatePyHandle').exclude() # Use GetHandle instead.
        except matcher.declaration_not_found_t:
            raise Exception('Class %s has no CreatePyHandle function. Did you forgot to declare the entity as a Python class?')
        
        # Apply common rules to the entity class
        # Don't care about the following:
        cls.vars(lambda decl: 'NetworkVar' in decl.name, allow_empty=True).exclude()        # Don't care or needs a better look
        cls.classes(lambda decl: 'NetworkVar' in decl.name, allow_empty=True).exclude()        # Don't care or needs a better look
        cls.mem_funs(lambda decl: 'YouForgotToImplement' in decl.name, allow_empty=True).exclude()   # Don't care
        #cls.mem_funs('ClearPyInstance').exclude()        # Not needed, used for cleaning up python entities
        cls.mem_funs('GetBaseMap', allow_empty=True).exclude()             # Not needed
        cls.mem_funs('GetDataDescMap', allow_empty=True).exclude()         # Not needed
        cls.mem_funs('GetDataDescMap', allow_empty=True).exclude()         # Not needed

        
        # 
        #cls.mem_funs(matchers.calldef_matcher_t(return_type='::%s *' % (clsname))).exclude()
        #cls.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(cls)))).call_policies = call_policies.return_value_policy(call_policies.return_by_value)

        matrix3x4 = mb.class_('matrix3x4_t')
        cls.calldefs(matchers.calldef_matcher_t(return_type=reference_t(declarated_t(matrix3x4))), allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.return_by_value) 
        
        cls.vars(allow_empty=True).exclude()
        
        return cls
            
    def ParseClientEntities(self, mb):
        # Made not virtual so no wrapper code is generated in IClientUnknown and IClientEntity
        mb.class_('IClientRenderable').mem_funs().virtuality = 'not virtual' 
        mb.class_('IClientNetworkable').mem_funs().virtuality = 'not virtual' 
        mb.class_('IClientThinkable').mem_funs().virtuality = 'not virtual'

        self.IncludeEmptyClass(mb, 'IClientUnknown')
        self.IncludeEmptyClass(mb, 'IClientEntity')
        
        for clsname in self.cliententities:
            cls = self.SetupEntityClass(mb, clsname)

            # Check if the python class is networkable. Add code for getting the "ClientClass" if that's the case.
            decl = cls.mem_funs('GetPyNetworkType', allow_empty=True)
            if decl:
                decl.include()
                cls.add_wrapper_code( tmpl_clientclass % {'clsname' : clsname})
                
            # Apply common rules
            # Excludes
            cls.mem_funs('GetPredDescMap', allow_empty=True).exclude()
            cls.mem_funs('OnNewModel', allow_empty=True).exclude() # Don't care for now
            cls.mem_funs('GetClientClass', allow_empty=True).exclude()
            cls.mem_funs('GetMouth', allow_empty=True).exclude()

        mb.mem_funs('SetThinkHandle').exclude()
        mb.mem_funs('GetThinkHandle').exclude()
            
    def ParseServerEntities(self, mb):
        self.IncludeEmptyClass(mb, 'IServerUnknown')
        self.IncludeEmptyClass(mb, 'IServerEntity')
        
        for clsname in self.serverentities:
            cls = self.SetupEntityClass(mb, clsname)
            
            # Check if the python class is networkable. Add code for getting the "ServerClass" if that's the case.
            decl = cls.mem_funs('GetPyNetworkType', allow_empty=True)
            if decl:
                decl.include()
                cls.add_wrapper_code(tmpl_serverclass % {'clsname' : clsname})
                
            # Apply common rules
            # Excludes
            cls.mem_funs('GetServerClass', allow_empty=True).exclude()         # Don't care about this one

        # Creation and spawning
        mb.free_functions('CreateEntityByName').include()
        mb.free_functions('DispatchSpawn').include()
        
    def ParseBaseEntityHandles(self, mb):
        # Dead entity
        cls = mb.class_('DeadEntity')
        cls.include()
        cls.mem_fun('NonZero').rename('__nonzero__')
        
        # Entity Handles
        cls = mb.class_('CBaseHandle')
        cls.include()
        cls.mem_funs().exclude()
        cls.mem_funs('GetEntryIndex').include()
        cls.mem_funs('GetSerialNumber').include()
        cls.mem_funs('ToInt').include()
        cls.mem_funs('IsValid').include()
        
        cls = mb.class_('PyHandle')
        cls.include()
        cls.mem_fun('Get').exclude()
        cls.mem_fun('PyGet').rename('Get')
        cls.mem_fun('GetAttr').rename('__getattr__')
        cls.mem_fun('GetAttribute').rename('__getattribute__')
        cls.mem_fun('SetAttr').rename('__setattr__')
        cls.mem_fun('Cmp').rename('__cmp__')
        cls.mem_fun('NonZero').rename('__nonzero__')
        cls.mem_fun('Str').rename('__str__')
        cls.mem_funs('GetPySelf').exclude()
        
        cls.add_wrapper_code(
            'virtual PyObject *GetPySelf() { return boost::python::detail::wrapper_base_::get_owner(*this); }'
        )
        
    def ParseBaseEntity(self, mb):
        # Exclude operators
        mb.global_ns.mem_opers('new').exclude()
        mb.global_ns.mem_opers('delete').exclude()
    
        cls = mb.class_('C_BaseEntity') if self.isclient else mb.class_('CBaseEntity')
    
        # List of shared functions overridable in Python
        mb.mem_funs('Precache').virtuality = 'virtual'
        mb.mem_funs('Spawn').virtuality = 'virtual'
        mb.mem_funs('Activate').virtuality = 'virtual'
        mb.mem_funs('KeyValue').virtuality = 'virtual'
        mb.mem_funs('UpdateOnRemove').virtuality = 'virtual'
        mb.mem_funs('CreateVPhysics').virtuality = 'virtual'
        mb.mem_funs('GetTracerType').virtuality = 'virtual'
        mb.mem_funs('MakeTracer').virtuality = 'virtual'
        mb.mem_funs('DoImpactEffect').virtuality = 'virtual'
        mb.mem_funs('StartTouch').virtuality = 'virtual'
        mb.mem_funs('EndTouch').virtuality = 'virtual'
        mb.mem_funs('UpdateTransmitState').virtuality = 'virtual'
        mb.mem_funs('ComputeWorldSpaceSurroundingBox').virtuality = 'virtual'
        
        # Call policies
        cls.mem_funs('CollisionProp').call_policies = call_policies.return_internal_reference()
        
        mb.mem_funs('GetTouchTrace').call_policies = call_policies.return_value_policy(call_policies.reference_existing_object)  # Temp fix, relative unsafe
        
        # Excludes
        mb.mem_funs('GetDataObject').exclude() # Don't care
        mb.mem_funs('CreateDataObject').exclude() # Don't care
        mb.mem_funs('DestroyDataObject').exclude() # Don't care
        mb.mem_funs('DestroyAllDataObjects').exclude() # Don't care
        mb.mem_funs('AddDataObjectType').exclude() # Don't care
        mb.mem_funs('RemoveDataObjectType').exclude() # Don't care
        mb.mem_funs('HasDataObjectType').exclude() # Don't care
        cls.mem_funs('GetPyInstance').exclude()          # Not needed, used when converting entities to python
        mb.mem_funs('DestroyPyInstance').exclude()        # Not needed, used for cleaning up python entities
        cls.mem_funs('PyAllocate').exclude()             # Python Intern only
        cls.mem_funs('PyDeallocate').exclude()             # Python Intern only
        cls.mem_funs('GetRefEHandle').exclude()          # We already got an auto conversion to a safe handle
        cls.mem_funs('GetBeamTraceFilter').exclude()     # Don't care
        cls.mem_funs('GetCollideable').exclude()         # Don't care for now
        cls.mem_funs('GetModel').exclude()               # Do we want this? 
        cls.mem_funs('GetTeam').exclude()     # Don't care about CTeam for now
        cls.mem_funs('AddEntityToGroundList').exclude()
        cls.mem_funs('ParseMapData').exclude() # Won't call this from python, needs CEntityMapData * argument
        
        # Returning a physics object -> Convert by value, which results in the wrapper object being returned
        physicsobject = mb.class_('IPhysicsObject')
        mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(physicsobject))), allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.return_by_value)
        
        # Rename python methods to match the c++ names ( but in c++ they got python prefixes )
        mb.mem_funs('SetPyTouch').rename('SetTouch')
        mb.mem_funs('SetPyThink').rename('SetThink')
        mb.mem_funs('GetPyThink').rename('GetThink')
        mb.mem_funs('PyThink').exclude()
        mb.mem_funs('PyTouch').exclude()
        
        if self.isclient:
            cls.mem_funs('ParticleProp').call_policies = call_policies.return_internal_reference() 
            
            # List of client functions overridable in Python
            mb.mem_funs('ShouldDraw').virtuality = 'virtual' # Called when visibility is updated, doesn't happens a lot.
            mb.mem_funs('GetCollideType').virtuality = 'virtual'
            mb.mem_funs('ClientThink').virtuality = 'virtual'
            mb.mem_funs('OnDataChanged').virtuality = 'virtual'
            mb.mem_funs('Simulate').virtuality = 'virtual'
            
            # Excludes
            cls.mem_funs('Release').exclude()
            cls.mem_funs('FirstShadowChild').exclude()
            cls.mem_funs('GetClientNetworkable').exclude()
            cls.mem_funs('GetClientRenderable').exclude()
            cls.mem_funs('GetClientThinkable').exclude()
            cls.mem_funs('GetClientVehicle').exclude()
            cls.mem_funs('GetOriginInterpolator').exclude()
            cls.mem_funs('GetPVSNotifyInterface').exclude()
            cls.mem_funs('GetRenderClipPlane').exclude() # Pointer to 4 floats, requires manual conversion...
            cls.mem_funs('GetRotationInterpolator').exclude()
            cls.mem_funs('GetShadowParent').exclude()
            cls.mem_funs('GetThinkHandle').exclude()
            cls.mem_funs('GetVarMapping').exclude()
            cls.mem_funs('GetDataTableBasePtr').exclude()
            cls.mem_funs('GetOriginalNetworkDataObject').exclude()
            cls.mem_funs('GetPredictedFrame').exclude()
            cls.mem_funs('NextShadowPeer').exclude()
            cls.mem_funs('PhysicsMarkEntityAsTouched').exclude() # Don't care for now
            cls.mem_funs('RenderHandle').exclude()
            mb.mem_funs('PhysicsAddHalfGravity').exclude()  # No definition on the client!
            cls.mem_funs('PyUpdateNetworkVar').exclude()     # Internal for network vars
            cls.mem_funs('SetModelPointer').exclude() # Likely never needed, can use SetModel or SetModelIndex

            cls.mem_funs('AttemptToPowerup').exclude() # CDamageModifier has no class on the client...
        else:
            # List of server functions overridable in Python
            mb.mem_funs('PostConstructor').virtuality = 'virtual'
            mb.mem_funs('PostClientActive').virtuality = 'virtual'
            #mb.mem_funs('HandleAnimEvent').virtuality = 'virtual'
            mb.mem_funs('StopLoopingSounds').virtuality = 'virtual'
            mb.mem_funs('Event_Killed').virtuality = 'virtual'
            mb.mem_funs('Event_Gibbed').virtuality = 'virtual'
            mb.mem_funs('PassesDamageFilter').virtuality = 'virtual'
            mb.mem_funs('OnTakeDamage').virtuality = 'virtual'
            mb.mem_funs('OnTakeDamage_Alive').virtuality = 'virtual'
            mb.mem_funs('StopLoopingSounds').virtuality = 'virtual'
            mb.mem_funs('VPhysicsCollision').virtuality = 'virtual'
            mb.mem_funs('CanBecomeRagdoll').virtuality = 'virtual'
            mb.mem_funs('BecomeRagdoll').virtuality = 'virtual'
            mb.mem_funs('ShouldGib').virtuality = 'virtual'
            mb.mem_funs('CorpseGib').virtuality = 'virtual'
            mb.mem_funs('DrawDebugGeometryOverlays').virtuality = 'virtual'
            mb.mem_funs('DrawDebugTextOverlays').virtuality = 'virtual'
        
            # Excludes
            cls.mem_funs('edict').exclude()          # Not needed
            cls.mem_funs('GetNetworkable').exclude()         # Don't care for now
            cls.mem_funs('MyNextBotPointer').exclude()     # Don't care
            cls.mem_funs('GetServerVehicle').exclude()     # Don't care
            cls.mem_funs('NetworkProp').exclude()            # Don't care
            cls.mem_funs('GetResponseSystem').exclude()         # Don't care for now
            cls.mem_funs('MyNextBotPointer').exclude()
            cls.mem_funs('IsInTeam').exclude()              # Don't care about CTeam fow now
            
            cls.vars('m_pTimedOverlay').exclude()

            # Excludes
            #excludetypes = [
            #    pointer_t(declarated_t(mb.class_('CDamageModifier'))),
            #]
            #mb.calldefs( calldef_withtypes( excludetypes ) ).exclude()
    
    def ParseBaseAnimating(self, mb):
        cls = mb.class_('C_BaseAnimating') if self.isclient else mb.class_('CBaseAnimating')
    
        # Transformations
        mb.mem_funs('GetPoseParameterRange').add_transformation(FT.output('minValue'), FT.output('maxValue'))
        
        # Give back a direct reference to CStudioHdr (not fully safe, but should be OK)
        studiohdr = mb.class_('CStudioHdr')
        mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(studiohdr))), allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.reference_existing_object)  
            
        # Exclude anything return CBoneCache
        bonecache = mb.class_('CBoneCache')
        mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(bonecache))), allow_empty=True).exclude()
            
        if self.isclient:
            # Client excludes
            cls.mem_fun('RemoveBoneAttachments').exclude() # No definition
        else:
            # Server excludes
            cls.mem_fun('GetEncodedControllerArray').exclude()
            cls.mem_fun('GetPoseParameterArray').exclude()
            
            mb.calldefs('GetBonePosition', matchers.calldef_matcher_t(arg_types=[pointer_t(const_t(declarated_t(char_t()))), None, None])).exclude() # No definition
            
    def ParseBaseAnimatingOverlay(self, mb):
        cls = mb.class_('C_BaseAnimatingOverlay') if self.isclient else mb.class_('CBaseAnimatingOverlay')
    
        cls.mem_funs('GetAnimOverlay').exclude()

    def ParseBaseFlex(self, mb):
        cls = mb.class_('C_BaseFlex') if self.isclient else mb.class_('CBaseFlex')

        excludetypes = [
            pointer_t(declarated_t(mb.class_('CChoreoScene'))),
            pointer_t(declarated_t(mb.class_('CChoreoActor'))),
        ]
        mb.calldefs( calldef_withtypes( excludetypes ) ).exclude()

    def ParseBaseCombatWeapon(self, mb):
        cls_name = 'C_BaseCombatWeapon' if self.isclient else 'CBaseCombatWeapon'
        cls = mb.class_(cls_name)
        
        # Overridable
        mb.mem_funs('PrimaryAttack').virtuality = 'virtual'
        mb.mem_funs('SecondaryAttack').virtuality = 'virtual'
        
        # Shared Excludes
        mb.mem_funs('ActivityList').exclude()
        mb.mem_funs('GetConstraint').exclude()
        mb.mem_funs('GetDeathNoticeName').exclude()
        mb.mem_funs('GetEncryptionKey').exclude()
        mb.mem_funs('GetProficiencyValues').exclude()
        
        if self.isclient:
            # Exclude anything returning a pointer to CHudTexture (don't care for now)
            hudtexture = mb.class_('CHudTexture')
            mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(hudtexture))), allow_empty=True).exclude()
            mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(const_t(declarated_t(hudtexture)))), allow_empty=True).exclude()
        else:
            # Exclude anything returning a pointer to CHudTexture
            mb.calldefs(matchers.calldef_matcher_t(return_type='::CHudTexture const *'), allow_empty=True).exclude()
            mb.calldefs(matchers.calldef_matcher_t(return_type='::CHudTexture *'), allow_empty=True).exclude()
            
            # Server excludes
            cls.mem_fun('GetDmgAccumulator').exclude()
            cls.mem_fun('RepositionWeapon').exclude() # No definition
            cls.mem_fun('IsInBadPosition').exclude() # No definition
            
    def ParseBaseCombatCharacter(self, mb):
        cls = mb.class_('C_BaseCombatCharacter' if self.isclient else 'CBaseCombatCharacter')
        
        # Shared excludes
        mb.mem_funs('GetVehicle').exclude()
        
        if self.isserver:
            # Server excludes
            cls.mem_fun('GetLastKnownArea').exclude()
            cls.mem_fun('RemoveWeapon').exclude() # No definition
            cls.mem_fun('CauseDeath').exclude() # No definition
            cls.mem_fun('OnPursuedBy').exclude() # No INextBot definition
        else:
            # When GLOWS_ENABLE define is added:
            if 'GLOWS_ENABLE' in mb.definedsymbols:
                mb.mem_funs('GetGlowObject', allow_empty=True).exclude()
                mb.mem_funs('GetGlowEffectColor', allow_empty=True).add_transformation( FT.output('r'), FT.output('g'), FT.output('b') )
            
    def ParseBasePlayer(self, mb):
        cls = mb.class_('C_BasePlayer') if self.isclient else mb.class_('CBasePlayer')
        
        # Shared excludes
        usercmd = mb.class_('CUserCmd')
        mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(const_t(declarated_t(usercmd)))), allow_empty=True).exclude()
        mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(usercmd))), allow_empty=True).exclude()
        
        cls.mem_fun('GetLadderSurface').exclude()
        cls.mem_fun('Hints').exclude()
        cls.mem_fun('GetSurfaceData').exclude()
        
        if self.isclient:
            # Remove anything returning a pointer to C_CommandContext
            commandcontext = mb.class_('C_CommandContext')
            mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(commandcontext))), allow_empty=True).exclude()
            
            # Client excludes
            cls.mem_fun('GetFogParams').exclude()
            cls.mem_fun('GetFootstepSurface').exclude()
            cls.mem_fun('GetHeadLabelMaterial').exclude()
            cls.mem_fun('GetRepresentativeRagdoll').exclude()
            cls.mem_fun('ShouldGoSouth').exclude() # No definition
        else:
            # Server excludes
            cls.mem_fun('GetExpresser').exclude()
            cls.mem_fun('GetBotController').exclude()
            cls.mem_fun('GetPlayerInfo').exclude()
            cls.mem_fun('GetPhysicsController').exclude()
            cls.mem_fun('PlayerData').exclude()
            cls.mem_fun('GetAudioParams').exclude()
            cls.mem_fun('SetWeaponAnimType').exclude() # No definition
            cls.mem_fun('SetTargetInfo').exclude() # No definition
            cls.mem_fun('SendAmmoUpdate').exclude() # No definition
            cls.mem_fun('DeathMessage').exclude() # No definition
            cls.mem_fun('SetupVPhysicsShadow').exclude() # Requires CPhysCollide, would need manually wrapping
            
    def ParseTriggers(self, mb):
        # CBaseTrigger
        cls_name = 'C_BaseTrigger' if self.isclient else 'CBaseTrigger'
        cls = mb.class_(cls_name)
        cls.no_init = False
            
    def ParseEntities(self, mb):
        self.ParseBaseEntityHandles(mb)
        
        self.IncludeEmptyClass(mb, 'IHandleEntity')
        
        if self.isclient:
            self.ParseClientEntities(mb)
        else:
            self.ParseServerEntities(mb)
            
        self.ParseBaseEntity(mb)
        self.ParseBaseAnimating(mb)
        self.ParseBaseAnimatingOverlay(mb)
        self.ParseBaseFlex(mb)
        self.ParseBaseCombatWeapon(mb)
        self.ParseBaseCombatCharacter(mb)
        self.ParseBasePlayer(mb)
        
        if self.isserver:
            self.ParseTriggers(mb)
        
    def Parse(self, mb):
        # Exclude everything by default
        mb.decls().exclude()
        
        self.ParseEntities(mb)
        
        # Finally apply common rules to all includes functions and classes, etc
        self.ApplyCommonRules(mb)
        
