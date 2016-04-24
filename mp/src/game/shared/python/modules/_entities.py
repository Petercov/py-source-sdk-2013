from srcpy.module_generators import SemiSharedModuleGenerator
from srcpy.matchers import calldef_withtypes

from pyplusplus import function_transformers as FT
from pyplusplus.module_builder import call_policies
from pygccxml.declarations import matcher, matchers, pointer_t, const_t, reference_t, declarated_t, char_t

# Templates for client and server class
# Special case: GetClientClass is called from different threads. Fallback to baseclass in this case.
# For most cases this does not matter because the send tables will be the same anyway.
tmpl_clientclass = '''virtual ClientClass* GetClientClass() {
#if defined(_WIN32)
        if( GetCurrentThreadId() != g_hPythonThreadID )
            return %(clsname)s::GetClientClass();
#endif // _WIN32
        if( PyObject_HasAttrString(GetPyInstance().ptr(), "pyClientClass") )
        {
            try
            {
                ClientClass *pClientClass = boost::python::extract<ClientClass *>( GetPyInstance().attr("pyClientClass") );
                if( pClientClass )
                    return pClientClass;
            }
            catch( bp::error_already_set & ) 
            {
                PyErr_Print();
            }
        }
        return %(clsname)s::GetClientClass();
    }
'''

tmpl_serverclass = '''virtual ServerClass* GetServerClass() {
        PY_OVERRIDE_CHECK( %(clsname)s, GetServerClass )
        if( PyObject_HasAttrString(GetPyInstance().ptr(), "pyServerClass") )
        {
            try
            {
                ServerClass *pServerClass = boost::python::extract<ServerClass *>( GetPyInstance().attr("pyServerClass") );
                if( pServerClass )
                    return pServerClass;
            }
            catch( bp::error_already_set & ) 
            {
                PyErr_Print();
            }
        }
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
#if PY_VERSION_HEX < 0x03000000
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
#else
        { //::%(handlename)s::Bool
        
            typedef bool ( ::%(handlename)s::*Bool_function_type )( ) const;
            
            %(handlename)s_exposer.def( 
                "__bool__"
                , Bool_function_type( &::%(handlename)s::Bool )
            );
        }
#endif // PY_VERSION_HEX < 0x03000000
        { //::%(handlename)s::Hash
        
            typedef Py_hash_t ( ::%(handlename)s::*Hash_function_type )( ) const;
            
            %(handlename)s_exposer.def( 
                "__hash__"
                , Hash_function_type( &::%(handlename)s::Hash )
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
        %(handlename)s_exposer.def( bp::self != bp::other< bp::api::object >() );
        %(handlename)s_exposer.def( bp::self == bp::other< bp::api::object >() );
    }
'''

tmpl_ent_converters_to = '''
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
'''

tmpl_ent_converters_from = '''
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
       if( h.Get() == NULL ) {
           return Py_None;
       }
       return h.Get();
    }
};
'''

class Entities(SemiSharedModuleGenerator):
    module_name = '_entities'
    split = True

    required_files = [
        '$SRCDIR\game\shared\python\srcpy_entities.cpp',
        '$SRCDIR\game\shared\python\srcpy_entities.h',
        '$SRCDIR\game\shared\python\srcpy_networkvar.cpp',
        '$SRCDIR\game\shared\python\srcpy_networkvar.h',
        '$SRCDIR\game\shared\python\srcpy_scclasses.cpp',
    ]

    @property
    def files(self):
        return filter(None, [
            'cbase.h',
            'npcevent.h',
            'srcpy_entities.h',
            'bone_setup.h',
            'baseprojectile.h',
            'basegrenade_shared.h',
            '$takedamageinfo.h',
            '$c_ai_basenpc.h',
            '#SkyCamera.h',
            '#ai_basenpc.h',
            '#modelentities.h',
            '$c_basetoggle.h' if self.settings.branch == 'swarm' else '',
            '#basetoggle.h',
            '$c_triggers.h' if self.settings.branch == 'swarm' else '',
            '#triggers.h',
            '$soundinfo.h',
            '#AI_Criteria.h',
            'saverestore.h',
            'saverestoretypes.h',
            'vcollide_parse.h', # solid_t
            '#iservervehicle.h',
            '$iclientvehicle.h',
            '%choreoscene.h',
            '%choreoactor.h',
            '$steam/steamclientpublic.h', # CSteamID
            '$view_shared.h', # CViewSetup
            '#gib.h',
            '#spark.h',
            '#filters.h',
            '#EntityFlame.h',
            '$c_playerresource.h',
            '#player_resource.h',
            '#props.h',
            '$c_breakableprop.h',
            '#physics_prop_ragdoll.h',
            '#nav_area.h',
            
            # For parsing only (used to exclude functions based on return value)
            '$%baseviewmodel_shared.h',
            '#%team.h',
            '$%c_team.h',
            '%mapentities_shared.h',
            '%ai_responsesystem.h' if self.settings.branch == 'swarm' else '%#ai_responsesystem.h',
        ])
        
    # List of entity classes want to have exposed
    cliententities = [ 
        'C_BaseEntity', 
        'C_BaseAnimating',
        'C_BaseAnimatingOverlay',
        'C_BaseFlex',
        'C_BaseCombatCharacter',
        'C_BaseCombatWeapon',
        'C_BaseProjectile',
        'C_BaseGrenade',
        'C_BasePlayer',
        'C_PlayerResource',
        'C_BreakableProp',
    ]
    
    serverentities = [ 
        'CBaseEntity', 
        'CBaseAnimating',
        'CBaseAnimatingOverlay',
        'CBaseFlex',
        'CBaseCombatCharacter',
        'CBaseCombatWeapon',
        'CBaseProjectile',
        'CBaseGrenade',
        'CBasePlayer',
        'CPlayerResource',
        'CPointEntity',
        'CServerOnlyEntity',
        'CServerOnlyPointEntity',
        'CLogicalEntity',
        'CFuncBrush',
        'CBaseToggle',
        'CBaseTrigger',
        'CTriggerMultiple',
        'CBaseFilter',
        'CGib',
        'CBaseProp',
        'CBreakableProp',
        'CPhysicsProp',
        'CRagdollProp',
        'CEntityFlame',
        
    ]
    
    def AddEntityConverter(self, mb, clsname, pyhandletoptronly=False):
        ''' Creates entities converters/handles for Python. '''
        cls = mb.class_(clsname)
        
        handlename = '%sHANDLE' % (clsname)
        
        ptr_convert_to_py_name = 'ptr_%s_to_handle' % (clsname)
        convert_to_py_name = '%s_to_handle' % (clsname)
        convert_from_py_name = 'handle_to_%s' % (clsname)
        
        if not pyhandletoptronly:
            # Add handle
            mb.add_declaration_code( 'typedef CEPyHandle< %s > %s;\r\n'% (clsname, handlename) )
            mb.add_registration_code( tmpl_enthandle % {'clsname' : clsname, 'handlename' : handlename}, True )
        
        # Add declaration code for converters
        if not pyhandletoptronly:
            mb.add_declaration_code( tmpl_ent_converters_to % {
                'clsname' : clsname,
                'ptr_convert_to_py_name' : ptr_convert_to_py_name,
                'convert_to_py_name' : convert_to_py_name,
                'convert_from_py_name' : convert_from_py_name,
            })
        
        mb.add_declaration_code( tmpl_ent_converters_from % {
            'clsname' : clsname,
            'ptr_convert_to_py_name' : ptr_convert_to_py_name,
            'convert_to_py_name' : convert_to_py_name,
            'convert_from_py_name' : convert_from_py_name,
        })
        
        # Add registration code
        if not pyhandletoptronly:
            mb.add_registration_code( "%s();" % (ptr_convert_to_py_name) )
            mb.add_registration_code( "%s();" % (convert_to_py_name) )
        mb.add_registration_code( "%s();" % (convert_from_py_name) )
        
    # Parse methods
    def SetupEntityClass(self, mb, clsname):
        ''' This function is called for both exposed client and server entities and 
            applies shared functionality. '''
        cls = mb.class_(clsname)
        
        self.entclasses.append(cls)
        
        cls.include()
        cls.calldefs(matchers.access_type_matcher_t('protected'), allow_empty=True).exclude()
        
        # Be selective about what we need to override
        # DO NOT REMOVE. Some functions are not thread safe, which will cause runtime errors because we did not setup python threadsafe (slower)
        cls.mem_funs(allow_empty=True).virtuality = 'not virtual' 

        # Add converters + a python handle class
        self.AddEntityConverter(mb, clsname)  
        
        # Use by converters to check if a Python Object is attached
        cls.add_wrapper_code('virtual PyObject *GetPySelf() const { return bp::detail::wrapper_base_::get_owner(*this); }')
        
        # Test if the Entity class is setup right
        try:
            cls.mem_funs('CreatePyHandle').exclude() # Use GetHandle instead.
        except (matcher.declaration_not_found_t, RuntimeError):
            raise Exception('Class %s has no CreatePyHandle function. Did you forgot to declare the entity as a Python class?' % (clsname))
        
        # Apply common rules to the entity class
        # Don't care about the following:
        cls.classes(lambda decl: 'NetworkVar' in decl.name, allow_empty=True).exclude()
        cls.mem_funs(lambda decl: 'YouForgotToImplement' in decl.name, allow_empty=True).exclude()
        cls.mem_funs(function=lambda decl: 'NetworkStateChanged_' in decl.name, allow_empty=True).exclude()
        cls.mem_funs('GetBaseMap', allow_empty=True).exclude()             # Not needed
        cls.mem_funs('GetDataDescMap', allow_empty=True).exclude()         # Not needed
        cls.mem_funs('GetDataDescMap', allow_empty=True).exclude()         # Not needed
        
        cls.mem_funs('DestroyPyInstance', allow_empty=True).exclude()      # Not needed, used for cleaning up python entities

        # matrix3x4_t is always returned by value
        matrix3x4 = mb.class_('matrix3x4_t')
        cls.calldefs(matchers.calldef_matcher_t(return_type=reference_t(declarated_t(matrix3x4))), allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.return_by_value) 
        cls.calldefs(matchers.calldef_matcher_t(return_type=reference_t(const_t(declarated_t(matrix3x4)))), allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.return_by_value) 
        
        # Exclude functions with CTeam, CUserCmd, edict_t
        usercmd = mb.class_('CUserCmd')
        edict = mb.class_('edict_t')
        groundlink = mb.class_('groundlink_t')
        touchlink = mb.class_('touchlink_t')
        bf_read = mb.class_('bf_read')
        ray = mb.class_('Ray_t')
        excludetypes = [
            pointer_t(declarated_t(mb.class_('CTeam' if self.isserver else 'C_Team'))),
            pointer_t(const_t(declarated_t(usercmd))),
            pointer_t(declarated_t(usercmd)),
            pointer_t(const_t(declarated_t(edict))),
            pointer_t(declarated_t(edict)),
            pointer_t(declarated_t(mb.class_('CEntityMapData'))),
            pointer_t(declarated_t(groundlink)),
            pointer_t(declarated_t(touchlink)),
            pointer_t(declarated_t(bf_read)),
            reference_t(declarated_t(bf_read)),
            reference_t(const_t(declarated_t(ray))),
            pointer_t(declarated_t(mb.class_('ICollideable'))),
        ]
        if self.settings.branch == 'swarm':
            # In source2013, this only exists on the server
            excludetypes.append(pointer_t(declarated_t(mb.class_('IResponseSystem'))))
        cls.calldefs(calldef_withtypes(excludetypes), allow_empty=True).exclude()
        
        # Returning a physics object -> Convert by value, which results in the wrapper object being returned
        physicsobject = mb.class_('IPhysicsObject')
        cls.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(physicsobject))), allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.return_by_value)
        
        # All public variables are excluded by default
        cls.vars(allow_empty=True).exclude()
        
        return cls
        
    def FindNetworkClass(self, mb, cls):
        # Test current class
        decl = cls.mem_funs('GetClientClass' if self.isclient else 'GetServerClass', allow_empty=True)
        if decl:
            return cls
            
        # Search bases
        for base in cls.bases:
            foundcls = self.FindNetworkClass(mb, base.related_class)
            if foundcls:
                return foundcls
        return None
                
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
            networkcls = self.FindNetworkClass(mb, cls)
            if networkcls:
                cls.add_wrapper_code(tmpl_clientclass % {'clsname' : networkcls.name, 'modulename' : self.module_name})
                
            # Apply common rules
            # Excludes
            cls.mem_funs('GetClientClass', allow_empty=True).exclude()
            cls.mem_funs('GetPredDescMap', allow_empty=True).exclude()
            cls.mem_funs('GetVarMapping', allow_empty=True).exclude()
            cls.mem_funs('GetDataTableBasePtr', allow_empty=True).exclude()
            cls.mem_funs('OnNewModel', allow_empty=True).exclude() # Don't care for now
            cls.mem_funs('GetMouth', allow_empty=True).exclude()
            
            # Remove anything returning a pointer to C_CommandContext
            commandcontext = mb.class_('C_CommandContext')
            cls.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(commandcontext))), allow_empty=True).exclude()
            
            # Exclude a list of functions with certain types
            interpvarvector = mb.class_('CInterpolatedVar< Vector >')
            interpvarqangle = mb.class_('CInterpolatedVar< QAngle >')
            excludetypes = [
                pointer_t(declarated_t(mb.class_('IClientRenderable'))),
                pointer_t(declarated_t(mb.class_('IClientNetworkable'))),
                pointer_t(declarated_t(mb.class_('IClientThinkable'))),
                pointer_t(declarated_t(mb.class_('IClientVehicle'))),
                pointer_t(const_t(declarated_t(mb.class_('IClientVehicle')))),
                pointer_t(declarated_t(mb.class_('IInterpolatedVar'))),
                pointer_t(declarated_t(interpvarvector)),
                reference_t(declarated_t(interpvarvector)),
                pointer_t(declarated_t(interpvarqangle)),
                reference_t(declarated_t(interpvarqangle)),
            ]
            cls.calldefs(calldef_withtypes(excludetypes), allow_empty=True).exclude()
            
        mb.mem_funs('SetThinkHandle').exclude()
        mb.mem_funs('GetThinkHandle').exclude()
            
    def ParseServerEntities(self, mb):
        self.IncludeEmptyClass(mb, 'IServerUnknown')
        self.IncludeEmptyClass(mb, 'IServerEntity')
        
        for clsname in self.serverentities:
            cls = self.SetupEntityClass(mb, clsname)
            
            # Check if the python class is networkable. Add code for getting the "ServerClass" if that's the case.
            networkcls = self.FindNetworkClass(mb, cls)
            if networkcls:
                cls.add_wrapper_code(tmpl_serverclass % {'clsname' : networkcls.name, 'modulename' : self.module_name})
                
            # Apply common rules
            cls.mem_funs('GetServerClass', allow_empty=True).exclude()
            cls.mem_funs('GetSendTable', allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.reference_existing_object)
            
            excludetypes = [
                pointer_t(declarated_t(mb.class_('IServerVehicle'))),
                pointer_t(const_t(declarated_t(mb.class_('IServerVehicle')))),
                pointer_t(declarated_t(mb.class_('IServerNetworkable'))),
                pointer_t(declarated_t(mb.class_('CEventAction'))),
                pointer_t(declarated_t(mb.class_('CCheckTransmitInfo'))),
                pointer_t(const_t(declarated_t(mb.class_('CCheckTransmitInfo')))),
                pointer_t(declarated_t(mb.class_('CNavArea'))),
                pointer_t(const_t(declarated_t(mb.class_('CNavArea')))),
            ]
            if self.settings.branch == 'source2013':
                # In swarm, this also exists on the server
                excludetypes.append(pointer_t(declarated_t(mb.class_('IResponseSystem'))))
            cls.calldefs(calldef_withtypes(excludetypes), allow_empty=True).exclude()

        # Spawning helper
        mb.free_functions('DispatchSpawn').include()

    def ParseBaseEntityHandles(self, mb):
        # Dead entity
        cls = mb.class_('DeadEntity')
        cls.include()
        cls.mem_funs('NonZero', allow_empty=True).rename('__nonzero__') # Py2
        cls.mem_funs('Bool', allow_empty=True).rename('__bool__') # Py3
        
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
        cls.mem_funs('Cmp', allow_empty=True).rename('__cmp__') # Py2
        cls.mem_funs('NonZero', allow_empty=True).rename('__nonzero__') # Py2
        cls.mem_funs('Bool', allow_empty=True).rename('__bool__') # Py3
        cls.mem_fun('Hash').rename('__hash__')
        cls.mem_fun('Str').rename('__str__')
        
        cls.add_wrapper_code(
            'virtual PyObject *GetPySelf() { return boost::python::detail::wrapper_base_::get_owner(*this); }'
        )
    
    def ParseBaseEntity(self, mb):
        cls = mb.class_('C_BaseEntity' if self.isclient else 'CBaseEntity')
        
        # Exclude operators
        mb.global_ns.mem_opers('new').exclude()
        mb.global_ns.mem_opers('delete').exclude()
    
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
        mb.mem_funs('OnRestore').virtuality = 'virtual'
        mb.mem_funs('Restore').virtuality = 'virtual'
        
        # Call policies
        cls.mem_funs('CollisionProp').call_policies = call_policies.return_internal_reference()
        mb.mem_funs('GetBeamTraceFilter').call_policies = call_policies.return_value_policy(call_policies.return_by_value)
        mb.mem_funs('GetTouchTrace').call_policies = call_policies.return_value_policy(call_policies.reference_existing_object)  # unsafe
        
        # Rename python methods to match the c++ names ( but in c++ they got python prefixes )
        mb.mem_funs('SetPyTouch').rename('SetTouch')
        mb.mem_funs('SetPyThink').rename('SetThink')
        mb.mem_funs('GetPyThink').rename('GetThink')
        mb.mem_funs('GetPyHandle').rename('GetHandle')
        mb.mem_funs('PyThink').exclude()
        mb.mem_funs('PyTouch').exclude()
        
        # Excludes
        cls.mem_funs('GetPyInstance').exclude()          # Not needed, used when converting entities to python
        cls.mem_funs('SetPyInstance').exclude()          # Not needed, used when converting entities to python
        cls.mem_funs('PyAllocate').exclude()             # Python Intern only
        cls.mem_funs('PyDeallocate').exclude()           # Python Intern only
        
        mb.mem_funs('GetRefEHandle').exclude()          # We already got an auto conversion to a safe handle
        mb.mem_funs('SetRefEHandle').exclude()          # We already got an auto conversion to a safe handle
        mb.mem_funs('GetModel').exclude()               # Probably not needed

        mb.mem_funs('GetBaseEntity').exclude()          # Automatically done by converter
        mb.mem_funs('GetBaseAnimating').exclude() # Automatically done by converter
        mb.mem_funs('MyCombatCharacterPointer').exclude() # Automatically done by converter
        mb.mem_funs('MyNPCPointer').exclude()
        mb.mem_funs('MyCombatWeaponPointer').exclude() # Automatically done by converter
        
        mb.mem_funs('ThinkSet').exclude()               # Replaced by SetPyThink
        mb.mem_funs('PhysicsRunThink').exclude()            # Don't care  
        mb.mem_funs('PhysicsRunSpecificThink').exclude()    # Don't care   
        mb.mem_funs('PhysicsDispatchThink').exclude()   # Don't care
        mb.mem_funs('VPhysicsGetObjectList').exclude()  # Don't care for now
        
        mb.mem_funs('GetDataObject').exclude() # Don't care
        mb.mem_funs('CreateDataObject').exclude() # Don't care
        mb.mem_funs('DestroyDataObject').exclude() # Don't care
        mb.mem_funs('DestroyAllDataObjects').exclude() # Don't care
        mb.mem_funs('AddDataObjectType').exclude() # Don't care
        mb.mem_funs('RemoveDataObjectType').exclude() # Don't care
        mb.mem_funs('HasDataObjectType').exclude() # Don't care
        
        mb.mem_funs('NetworkStateChanged').exclude() # void * argument
        
        if self.settings.branch == 'source2013':
            mb.mem_funs('GetHasAttributesInterfacePtr').exclude()
        
        # Use isclient/isserver globals/builtins
        mb.mem_funs('IsServer').exclude() 
        mb.mem_funs('IsClient').exclude() 
        mb.mem_funs('GetDLLType').exclude() 
        
        # Transform EmitSound
        # There seems to be a problem with static and member functions with the same name
        # Rename EmitSound with filter into "EmitSoundFilter"
        # Rename static StopSound to StopSoundStatic
        decls = mb.mem_funs('EmitSound')
        
        mb.mem_funs('EmitSound', calldef_withtypes(reference_t(declarated_t(mb.class_('IRecipientFilter'))))).rename('EmitSoundFilter')
        mb.mem_funs('StopSound', lambda decl: decl.has_static).rename('StopSoundStatic')
        
        for decl in decls:
            for arg in decl.arguments:
                if arg.name == 'duration':
                    decl.add_transformation(FT.output('duration'))
        mb.typedef('HSOUNDSCRIPTHANDLE').include()
        
        # Create properties for the following variables, since they are networked
        for entcls in self.entclasses:
            if entcls == cls or next((x for x in entcls.recursive_bases if x.related_class == cls), None):
                self.AddNetworkVarProperty('lifestate', 'm_lifeState', 'int', entcls)
                self.AddNetworkVarProperty('takedamage', 'm_takedamage', 'int', entcls)
        
        if self.isclient:
            cls.mem_funs('ParticleProp').call_policies = call_policies.return_internal_reference() 
            
            # List of client functions overridable in Python
            mb.mem_funs('ShouldDraw').virtuality = 'virtual' # Called when visibility is updated, doesn't happens a lot.
            mb.mem_funs('GetCollideType').virtuality = 'virtual'
            mb.mem_funs('ClientThink').virtuality = 'virtual'
            mb.mem_funs('OnDataChanged').virtuality = 'virtual'
            mb.mem_funs('Simulate').virtuality = 'virtual'
            mb.mem_funs('NotifyShouldTransmit').virtuality = 'virtual'
            mb.mem_funs('PyReceiveMessage').virtuality = 'virtual'
            mb.mem_funs('PyReceiveMessage').rename('ReceiveMessage')

            # Excludes
            mb.mem_funs('Release').exclude() # Should not be called directly from Python
            cls.mem_funs('GetIClientUnknown').exclude()
            cls.mem_funs('GetIClientEntity').exclude()
            cls.mem_funs('GetClientHandle').exclude()
            cls.mem_funs('RenderHandle').exclude()
            cls.mem_funs('RemoveVar').exclude()
            
            cls.mem_funs('GetPVSNotifyInterface').exclude()
            cls.mem_funs('GetRenderClipPlane').exclude() # Pointer to 4 floats, requires manual conversion...
            cls.mem_funs('GetIDString').exclude()
            cls.mem_funs('PhysicsAddHalfGravity').exclude() # No definition on the client
            cls.mem_funs('SetModelPointer').exclude() # Likely never needed, can use SetModel or SetModelIndex
            mb.mem_funs('OnNewModel').exclude() # TODO
            cls.mem_fun('OnNewParticleEffect').exclude()
            if self.settings.branch == 'swarm':
                cls.mem_fun('OnParticleEffectDeleted').exclude()
            
            mb.mem_funs('AllocateIntermediateData').exclude()
            mb.mem_funs('DestroyIntermediateData').exclude()
            mb.mem_funs('ShiftIntermediateDataForward').exclude()
            mb.mem_funs('GetPredictedFrame').exclude()
            mb.mem_funs('GetOriginalNetworkDataObject').exclude()
            mb.mem_funs('IsIntermediateDataAllocated').exclude()
            cls.mem_funs('AttemptToPowerup').exclude() # CDamageModifier has no class on the client...
            
            mb.mem_funs('PyUpdateNetworkVar').exclude() # Internal for network vars
            mb.mem_funs('PyNetworkVarChanged').exclude() # Internal for network vars
            
            if self.settings.branch == 'swarm':
                mb.mem_funs('GetClientAlphaProperty').exclude()
                mb.mem_funs('GetClientModelRenderable').exclude()
                mb.mem_funs('GetResponseSystem').exclude()
                mb.mem_funs('GetScriptDesc').exclude()
                mb.mem_funs('GetScriptInstance').exclude()
                mb.mem_funs('AlphaProp').exclude()
                
            # Not interested in Interpolation related functions
            mb.mem_funs(lambda decl: decl.name.startswith('Interp_')).exclude()
            # Not interested in RecvProxy functions
            mb.mem_funs(lambda decl: decl.name.startswith('RecvProxy_')).exclude()
                
            # Transform
            mb.mem_funs('GetShadowCastDistance').add_transformation(FT.output('pDist'))
            
            # Rename public variables
            self.IncludeVarAndRename('m_iHealth', 'health')
            self.IncludeVarAndRename('m_nRenderFX', 'renderfx')
            if self.settings.branch == 'source2013':
                self.IncludeVarAndRename('m_nRenderFXBlend', 'renderfxblend')
            self.IncludeVarAndRename('m_nRenderMode', 'rendermode')
            self.IncludeVarAndRename('m_clrRender', 'clrender')
            self.IncludeVarAndRename('m_flAnimTime', 'animtime')
            self.IncludeVarAndRename('m_flOldAnimTime', 'oldanimtime')
            self.IncludeVarAndRename('m_flSimulationTime', 'simulationtime')
            self.IncludeVarAndRename('m_flOldSimulationTime', 'oldsimulationtime')
            self.IncludeVarAndRename('m_nNextThinkTick', 'nextthinktick')
            self.IncludeVarAndRename('m_nLastThinkTick', 'lastthinktick')  
            self.IncludeVarAndRename('m_iClassname', 'classname')    
            self.IncludeVarAndRename('m_flSpeed', 'speed')

            # Client thinking vars
            mb.add_registration_code( "bp::scope().attr( \"CLIENT_THINK_ALWAYS\" ) = CLIENT_THINK_ALWAYS;" )
            mb.add_registration_code( "bp::scope().attr( \"CLIENT_THINK_NEVER\" ) = CLIENT_THINK_NEVER;" )
            
            if self.settings.branch == 'swarm':
                # Entity lists, swarm only
                mb.mem_funs('AddToEntityList').include()
                mb.mem_funs('RemoveFromEntityList').include()
                mb.enum('entity_list_ids_t').include()
        else:
            cls.mem_funs('PySendEvent').include()
            cls.mem_funs('PySendEvent').rename('SendEvent')
            self.IncludeVarAndRename('m_flPrevAnimTime', 'prevanimtime')
            self.IncludeVarAndRename('m_nNextThinkTick', 'nextthinktick')
            self.IncludeVarAndRename('m_nLastThinkTick', 'lastthinktick')
            self.IncludeVarAndRename('m_iClassname', 'classname')
            self.IncludeVarAndRename('m_iGlobalname', 'globalname')
            self.IncludeVarAndRename('m_iParent', 'parent')
            self.IncludeVarAndRename('m_iHammerID', 'hammerid')
            self.IncludeVarAndRename('m_flSpeed', 'speed')
            self.IncludeVarAndRename('m_debugOverlays', 'debugoverlays')
            self.IncludeVarAndRename('m_bAllowPrecache', 'allowprecache')
            self.IncludeVarAndRename('m_bInDebugSelect', 'indebugselect')
            self.IncludeVarAndRename('m_nDebugPlayer', 'debugplayer')
            self.IncludeVarAndRename('m_target', 'target')
            self.IncludeVarAndRename('m_iszDamageFilterName', 'damagefiltername')

            # Properties
            self.SetupProperty(cls, 'health', 'GetHealth', 'SetHealth')
            self.SetupProperty(cls, 'maxhealth', 'GetMaxHealth', 'SetMaxHealth')
            self.SetupProperty(cls, 'animtime', 'GetAnimTime', 'SetAnimTime')
            self.SetupProperty(cls, 'simulationtime', 'GetSimulationTime', 'SetSimulationTime')
            self.SetupProperty(cls, 'rendermode', 'GetRenderMode', 'SetRenderMode', excludesetget=False)
            
            mb.mem_funs('PySendMessage').rename('SendMessage')
            
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
            mb.mem_funs('ModifyOrAppendCriteria').virtuality = 'virtual'
            mb.mem_funs('DeathNotice').virtuality = 'virtual'
        
            # Excludes
            cls.mem_funs('NetworkProp').exclude()
            cls.mem_funs('MyNextBotPointer').exclude()
            mb.mem_funs('NotifySystemEvent').exclude()
            mb.mem_funs('Entity').exclude()
            cls.mem_fun('OnEntityEvent').exclude()
            
            mb.mem_funs('PhysicsTestEntityPosition').exclude()  # Don't care  
            mb.mem_funs('PhysicsCheckRotateMove').exclude()     # Don't care  
            mb.mem_funs('PhysicsCheckPushMove').exclude()       # Don't care

            mb.mem_funs('ForceVPhysicsCollide').exclude() # Don't care
            mb.mem_funs('GetGroundVelocityToApply').exclude() # Don't care
            mb.mem_funs('GetMaxHealth').exclude() # Use property maxhealth
            #mb.mem_funs('SetModelIndex').exclude()
            
            if self.settings.branch == 'swarm':
                # Not interested in SendProxy_ functions
                mb.mem_funs(lambda decl: decl.name.startswith('SendProxy_')).exclude()
            
            if self.settings.branch == 'swarm':
                mb.mem_funs('GetEntityNameAsCStr').exclude() # Always use GetEntityName()
                
                mb.mem_funs('SendProxy_AnglesX').exclude()
                mb.mem_funs('SendProxy_AnglesY').exclude()
                mb.mem_funs('SendProxy_AnglesZ').exclude()
                
                mb.mem_funs('FindNamedOutput').exclude()
                mb.mem_funs('GetBaseAnimatingOverlay').exclude()
                mb.mem_funs('GetContextData').exclude()
                mb.mem_funs('GetScriptDesc').exclude()
                mb.mem_funs('GetScriptInstance').exclude()
                mb.mem_funs('GetScriptOwnerEntity').exclude()
                mb.mem_funs('GetScriptScope').exclude()
                mb.mem_funs('ScriptFirstMoveChild').exclude()
                mb.mem_funs('ScriptGetModelKeyValues').exclude()
                mb.mem_funs('ScriptGetMoveParent').exclude()
                mb.mem_funs('ScriptGetRootMoveParent').exclude()
                mb.mem_funs('ScriptNextMovePeer').exclude()
                mb.mem_funs('InputDispatchEffect').exclude() # No def?
            
            # Do not want the firebullets function with multiple arguments. Only the one with the struct.
            mb.mem_funs(name='FireBullets', function=calldef_withtypes('int')).exclude()
            
        mb.enum('MoveCollide_t').include()

    def ParseBaseAnimating(self, mb):
        cls = mb.class_('C_BaseAnimating' if self.isclient else 'CBaseAnimating')
    
        # Transformations
        mb.mem_funs('GetPoseParameterRange').add_transformation(FT.output('minValue'), FT.output('maxValue'))
        
        # Give back a direct reference to CStudioHdr (not fully safe, but should be OK)
        studiohdr = mb.class_('CStudioHdr')
        mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(studiohdr))), allow_empty=True).call_policies = call_policies.return_value_policy(call_policies.reference_existing_object)  
        
        # Create properties for the following variables, since they are networked
        if self.isclient or self.settings.branch != 'source2013':
            cls.mem_fun('GetSkin').exclude()
        for entcls in self.entclasses:
            if entcls == cls or next((x for x in entcls.recursive_bases if x.related_class == cls), None):
                self.AddNetworkVarProperty('skin', 'm_nSkin', 'int', entcls)    

        # Exclude anything return CBoneCache
        bonecache = mb.class_('CBoneCache')
        mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(bonecache))), allow_empty=True).exclude()
        
        # Transformations
        mb.mem_funs('ComputeHitboxSurroundingBox').add_transformation(FT.output('pVecWorldMins'), FT.output('pVecWorldMaxs'))
        mb.mem_funs('ComputeEntitySpaceHitboxSurroundingBox').add_transformation(FT.output('pVecWorldMins'), FT.output('pVecWorldMaxs'))
        
        if self.isclient:
            # Exclude
            if self.settings.branch == 'swarm':
                mb.mem_funs('GetBoneArrayForWrite').exclude()
                mb.mem_funs('GetBoneForWrite').exclude()
            cls.mem_fun('RemoveBoneAttachments').exclude() # No definition
        else:
            if self.settings.branch == 'swarm':
                mb.mem_funs('OnSequenceSet').virtuality = 'virtual'
            
            # Server excludes
            cls.mem_fun('GetEncodedControllerArray').exclude()
            cls.mem_fun('GetPoseParameterArray').exclude()

            if self.settings.branch == 'swarm':
                mb.mem_funs('GetBoneCache').exclude()
                mb.mem_funs('InputIgniteNumHitboxFires').exclude()
                mb.mem_funs('InputIgniteHitboxFireScale').exclude()
                
            excludetypes = [pointer_t(const_t(declarated_t(char_t())))]
            mb.calldefs(name='GetBonePosition', function=calldef_withtypes(excludetypes)).exclude()
        
            # Rename vars
            self.IncludeVarAndRename('m_OnIgnite', 'onignite')
            self.IncludeVarAndRename('m_flGroundSpeed', 'groundspeed')
            self.IncludeVarAndRename('m_flLastEventCheck', 'lastevencheck')
            
            # Transformations
            mb.mem_funs('GotoSequence').add_transformation(FT.output('iNextSequence'), FT.output('flCycle'), FT.output('iDir'))
            mb.mem_funs('LookupHitbox').add_transformation(FT.output('outSet'), FT.output('outBox'))
            mb.mem_funs('GetIntervalMovement').add_transformation(FT.output('bMoveSeqFinished'))
            
            # Enums
            mb.enums('LocalFlexController_t').include()
        
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
        
        if self.isserver:
            mb.mem_funs('FlexSettingLessFunc').exclude()
            cls.class_('FS_LocalToGlobal_t').exclude()
            
            cls_ai_response = mb.typedef('AI_Response') if self.settings.branch == 'swarm' else mb.class_('AI_Response')
            excludetypes = [pointer_t(declarated_t(cls_ai_response))]
            mb.calldefs(function=calldef_withtypes(excludetypes)).exclude()
            if self.settings.branch == 'swarm':
                mb.mem_funs('ScriptGetOldestScene').exclude()
                mb.mem_funs('ScriptGetSceneByIndex').exclude()
            
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
        mb.mem_funs('GetControlPanelClassName').exclude()
        mb.mem_funs('GetControlPanelInfo').exclude()
        if self.settings.branch == 'source2013':
            mb.mem_funs('PoseParamList').exclude()
                
        if self.isclient:
            # Exclude anything returning a pointer to CHudTexture (don't care for now)
            hudtexture = mb.class_('CHudTexture')
            mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(declarated_t(hudtexture))), allow_empty=True).exclude()
            mb.calldefs(matchers.calldef_matcher_t(return_type=pointer_t(const_t(declarated_t(hudtexture)))), allow_empty=True).exclude()
            
            if self.settings.branch == 'swarm':
                mb.mem_funs('GetWeaponList').exclude() # Returns a CUtlLinkedList
        else:
            # Exclude anything returning a pointer to CHudTexture
            mb.calldefs(matchers.calldef_matcher_t(return_type='::CHudTexture const *'), allow_empty=True).exclude()
            mb.calldefs(matchers.calldef_matcher_t(return_type='::CHudTexture *'), allow_empty=True).exclude()
            
            # Server excludes
            mb.mem_funs('RepositionWeapon').exclude() # Declaration only...
            mb.mem_funs('IsInBadPosition').exclude() # Declaration only...
            if self.settings.branch == 'swarm':
                mb.mem_funs('IsCarrierAlive').exclude() # Declaration only..
            if self.settings.branch == 'source2013':
                mb.mem_funs('GetDmgAccumulator').exclude()
                
        # Rename variables
        self.IncludeVarAndRename('m_bAltFiresUnderwater', 'altfiresunderwater')
        self.IncludeVarAndRename('m_bFireOnEmpty', 'fireonempty')
        self.IncludeVarAndRename('m_bFiresUnderwater', 'firesunderwater')
        self.IncludeVarAndRename('m_bInReload', 'inreload')
        self.IncludeVarAndRename('m_bReloadsSingly', 'reloadssingly')
        self.IncludeVarAndRename('m_fFireDuration', 'fireduration')
        self.IncludeVarAndRename('m_fMaxRange1', 'maxrange1')
        self.IncludeVarAndRename('m_fMaxRange2', 'maxrange2')
        self.IncludeVarAndRename('m_fMinRange1', 'minrange1')
        self.IncludeVarAndRename('m_fMinRange2', 'minrange2')
        self.IncludeVarAndRename('m_flNextEmptySoundTime', 'nextemptysoundtime')
        self.IncludeVarAndRename('m_flUnlockTime', 'unlocktime')
        self.IncludeVarAndRename('m_hLocker', 'locker')
        self.IncludeVarAndRename('m_iSubType', 'subtype')
        self.IncludeVarAndRename('m_iViewModelIndex', 'viewmodelindex')
        self.IncludeVarAndRename('m_iWorldModelIndex', 'worldmodelindex')
        self.IncludeVarAndRename('m_iszName', 'name')
        self.IncludeVarAndRename('m_nViewModelIndex', 'viewmodelindex')
        
        # Create properties for the following variables, since they are networked
        for entcls in self.entclasses:
            if entcls == cls or next((x for x in entcls.recursive_bases if x.related_class == cls), None):
                self.AddNetworkVarProperty('nextprimaryattack', 'm_flNextPrimaryAttack', 'float', entcls)
                self.AddNetworkVarProperty('nextsecondaryattack', 'm_flNextSecondaryAttack', 'float', entcls)
                self.AddNetworkVarProperty('timeweaponidle', 'm_flTimeWeaponIdle', 'float', entcls)
                self.AddNetworkVarProperty('state', 'm_iState', 'int', entcls)
                self.AddNetworkVarProperty('primaryammotype', 'm_iPrimaryAmmoType', 'int', entcls)
                self.AddNetworkVarProperty('secondaryammotype', 'm_iSecondaryAmmoType', 'int', entcls)
                self.AddNetworkVarProperty('clip1', 'm_iClip1', 'int', entcls)
                self.AddNetworkVarProperty('clip2', 'm_iClip2', 'int', entcls)
            
        # Misc
        mb.enum('WeaponSound_t').include()
        mb.enum('WeaponSound_t').rename('WeaponSound')
                         
    def ParseBaseCombatCharacter(self, mb):
        cls = mb.class_('C_BaseCombatCharacter' if self.isclient else 'CBaseCombatCharacter')

        
        if self.isserver:
            cls.member_function('SetActiveWeapon').exclude()
            self.SetupProperty(cls, 'activeweapon', 'GetActiveWeapon', 'SetActiveWeapon')
        
            # Server excludes
            cls.mem_fun('RemoveWeapon').exclude() # No definition
            cls.mem_fun('CauseDeath').exclude() # No definition
            cls.mem_fun('OnPursuedBy').exclude() # No INextBot definition
            cls.mem_fun('DispatchInteraction').exclude() # void * argument
            cls.mem_fun('HandleInteraction').exclude() # void * argument
            if self.settings.branch == 'swarm':
                cls.mem_fun('GetEntitiesInFaction').exclude()
                cls.mem_fun('GetFogTrigger').exclude()
                cls.mem_fun('PlayFootstepSound').exclude()
            
            mb.free_function('RadiusDamage').include()

            self.IncludeVarAndRename('m_bForceServerRagdoll', 'forceserverragdoll')
            self.IncludeVarAndRename('m_bPreventWeaponPickup', 'preventweaponpickup')
            
            # LIST OF SERVER FUNCTIONS TO OVERRIDE
            mb.mem_funs('Weapon_Equip').virtuality = 'virtual'
            mb.mem_funs('Weapon_Switch').virtuality = 'virtual'
            mb.mem_funs('Weapon_Drop').virtuality = 'virtual'
            mb.mem_funs('Event_KilledOther').virtuality = 'virtual'
        else:
            if self.settings.branch == 'source2013':
                # When GLOWS_ENABLE define is added:
                if 'GLOWS_ENABLE' in self.symbols:
                    mb.mem_funs('GetGlowObject', allow_empty=True).exclude()
                    mb.mem_funs('GetGlowEffectColor', allow_empty=True).add_transformation( FT.output('r'), FT.output('g'), FT.output('b'))
            
            self.SetupProperty(cls, 'activeweapon', 'GetActiveWeapon')
            
    def ParseBaseGrenade(self, mb):
        cls_name = 'C_BaseGrenade' if self.isclient else 'CBaseGrenade'
        cls = mb.class_(cls_name)
        
        self.SetupProperty(cls, 'damage', 'GetDamage', 'SetDamage')
        self.SetupProperty(cls, 'damageradius', 'GetDamageRadius', 'SetDamageRadius')
        
        # Overrides
        cls.mem_funs('Explode').virtuality = 'virtual'
            
    def ParseBasePlayer(self, mb):
        cls = mb.class_('C_BasePlayer') if self.isclient else mb.class_('CBasePlayer')
 
        self.IncludeVarAndRename('m_nButtons', 'buttons')
        self.IncludeVarAndRename('m_afButtonLast', 'buttonslast')
        self.IncludeVarAndRename('m_afButtonPressed', 'buttonspressed')
        self.IncludeVarAndRename('m_afButtonReleased', 'buttonsreleased')
        
        cls.mem_fun('GetLadderSurface').exclude()
        cls.mem_fun('Hints').exclude()
        if self.settings.branch == 'source2013' or self.isserver:
            cls.mem_fun('GetSurfaceData').exclude()
            
        excludetypes = [pointer_t(const_t(declarated_t(char_t())))]
        cls.calldefs(name='GetPlayerName', function=calldef_withtypes(excludetypes)).exclude()
        cls.mem_fun('PyGetPlayerName').rename('GetPlayerName')
        
        if self.isclient:
            # Client excludes
            cls.mem_fun('GetFogParams').exclude()
            cls.mem_fun('OverrideView').exclude()
            cls.mem_fun('GetFootstepSurface').exclude()
            cls.mem_fun('GetHeadLabelMaterial').exclude()
            cls.mem_fun('GetRepresentativeRagdoll').exclude()
            cls.mem_fun('ShouldGoSouth').exclude() # No definition
            
            if self.settings.branch == 'swarm':
                mb.mem_funs('ActivePlayerCombatCharacter').exclude()
                mb.mem_funs('GetActiveColorCorrection').exclude()
                mb.mem_funs('GetActivePostProcessController').exclude()
                mb.mem_funs('GetPotentialUseEntity').exclude()
                mb.mem_funs('GetSoundscapeListener').exclude()
                mb.mem_funs('GetSplitScreenPlayers').exclude()
                mb.mem_funs('GetViewEntity').exclude()
                mb.mem_funs('IsReplay').exclude()

            mb.mem_funs('CalcView').add_transformation(FT.output('zNear'), FT.output('zFar'), FT.output('fov'))
        else:
            # Overridable server functions
            mb.mem_funs('ClientCommand').virtuality = 'virtual'
        
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
            cls.mem_fun('GetViewModel').exclude()
            cls.mem_fun('GetGroundVPhysics').exclude()
            cls.mem_fun('SetupVPhysicsShadow').exclude() # Requires CPhysCollide, would need manually wrapping
            
            if self.settings.branch == 'swarm':
                mb.mem_funs('ActivePlayerCombatCharacter').exclude()
                mb.mem_funs('FindPickerAILink').exclude()
                mb.mem_funs('GetPlayerProxy').exclude()
                mb.mem_funs('GetSoundscapeListener').exclude()
                mb.mem_funs('GetSplitScreenPlayerOwner').exclude()
                mb.mem_funs('GetSplitScreenPlayers').exclude()
                mb.mem_funs('GetTonemapController').exclude()
                mb.mem_funs('FindPickerAINode').exclude()

    def ParseTriggers(self, mb):
        if self.isclient and self.settings.branch == 'source2013':
            return
            
        # CBaseTrigger
        cls_name = 'C_BaseTrigger' if self.isclient else 'CBaseTrigger'
        cls = mb.class_(cls_name)
        cls.no_init = False
        
        if self.settings.branch == 'swarm':
            if self.isserver:
                cls.mem_funs('GetTouchingEntities').exclude()
                cls.mem_funs('GetClientSidePredicted').exclude() 
                cls.mem_funs('SetClientSidePredicted').exclude() 
                cls.add_property( 'clientsidepredicted'
                                 , cls.mem_fun('GetClientSidePredicted')
                                 , cls.mem_fun('SetClientSidePredicted') )
            else:
                self.IncludeVarAndRename('m_bClientSidePredicted', 'clientsidepredicted')

        # CTriggerMultiple
        if self.isserver:
            cls = mb.class_('CTriggerMultiple')
            mb.class_('CTriggerMultiple').no_init = False
            self.IncludeVarAndRename('m_bDisabled', 'disabled')
            self.IncludeVarAndRename('m_hFilter', 'filter')
            self.IncludeVarAndRename('m_iFilterName', 'filtername')
            
            for clsname in ['CBaseTrigger', 'CTriggerMultiple']:
                triggers = mb.class_(clsname)
                triggers.add_wrapper_code(    
                'virtual boost::python::list GetTouchingEntities( void ) {\r\n' + \
                '    return UtlVectorToListByValue<EHANDLE>(m_hTouchingEntities);\r\n' + \
                '}\r\n'        
                )
                triggers.add_registration_code(
                    'def( \r\n'
                    '    "GetTouchingEntities"\r\n'
                    '    , (boost::python::list ( ::%s_wrapper::* )( void ) )(&::%s_wrapper::GetTouchingEntities)\r\n'
                    ') \r\n' % (clsname, clsname)
                )
                         
    def ParseProps(self, mb):
        if self.isserver:
            cls = mb.class_('CBreakableProp')
            cls.mem_funs('GetRootPhysicsObjectForBreak').exclude()
            
            cls = mb.class_('CPhysicsProp')
                
            cls = mb.class_('CRagdollProp')
            cls.mem_funs('GetRagdoll').call_policies = call_policies.return_value_policy(call_policies.return_by_value)
            
            # Props
            mb.free_functions('PropBreakablePrecacheAll').include()
            
    def ParseFuncBrush(self, mb):
        if self.isserver:
            # CFuncBrush  
            mb.class_('CFuncBrush').vars('m_iSolidity').rename('solidity')
            mb.class_('CFuncBrush').vars('m_iDisabled').rename('disabled')
            mb.class_('CFuncBrush').vars('m_bSolidBsp').rename('solidbsp')
            mb.class_('CFuncBrush').vars('m_iszExcludedClass').rename('excludedclass')
            mb.class_('CFuncBrush').vars('m_bInvertExclusion').rename('invertexclusion')

            mb.add_registration_code( "bp::scope().attr( \"SF_WALL_START_OFF\" ) = (int)SF_WALL_START_OFF;" )
            mb.add_registration_code( "bp::scope().attr( \"SF_IGNORE_PLAYERUSE\" ) = (int)SF_IGNORE_PLAYERUSE;" )
            
    def ParseFilters(self, mb):
        if self.isserver:
            # Base filter
            cls = mb.class_('CBaseFilter')
            cls.no_init = False
            cls.mem_funs('PassesFilterImpl').virtuality = 'virtual' 
            cls.mem_funs('PassesDamageFilterImpl').virtuality = 'virtual' 
        
    def ParseRemainingEntities(self, mb):
        if self.isserver:
            # Not sure where to put this
            mb.free_function('DoSpark').include()
        
            # CSoundEnt
            self.IncludeEmptyClass(mb, 'CSoundEnt')
            mb.mem_funs('InsertSound').include()
            
            # CGib
            mb.free_functions('CreateRagGib').include()
            mb.enum('GibType_e').include()
        else:
            # C_PlayerResource
            cls = mb.class_('C_PlayerResource')
            cls.mem_fun('GetPlayerName').exclude()
            cls.mem_fun('PyGetPlayerName').rename('GetPlayerName')
            mb.add_declaration_code( "C_PlayerResource *wrap_PlayerResource( void )\r\n{\r\n\treturn g_PR;\r\n}\r\n" )
            mb.add_registration_code( 'bp::def( "PlayerResource", wrap_PlayerResource, bp::return_value_policy< bp::return_by_value >() );' )
            
            
    def ParseEntities(self, mb):
        self.ParseBaseEntityHandles(mb)
        
        self.IncludeEmptyClass(mb, 'IHandleEntity')
        self.AddEntityConverter(mb, 'IHandleEntity', True)
        
        mb.free_functions('CreateEntityByName').include()
        
        self.entclasses = []
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
        self.ParseBaseGrenade(mb)
        self.ParseBasePlayer(mb)
        self.ParseTriggers(mb)
        self.ParseProps(mb)
        self.ParseFuncBrush(mb)
        self.ParseFilters(mb)
        self.ParseRemainingEntities(mb)
        
    def Parse(self, mb):
        # Exclude everything by default
        mb.decls().exclude()
        
        self.ParseEntities(mb)
        
        # Protected functions we do want:
        if self.isserver:
            mb.mem_funs('TraceAttack').include()
            mb.mem_funs('PassesFilterImpl').include()
            mb.mem_funs('PassesDamageFilterImpl').include()
        
        # Finally apply common rules to all includes functions and classes, etc.
        self.ApplyCommonRules(mb)
        
