// This file has been generated by Py++.

#include "cbase.h"
// This file has been generated by Py++.

#include "cbase.h"
#include "npcevent.h"
#include "srcpy_entities.h"
#include "bone_setup.h"
#include "baseprojectile.h"
#include "basegrenade_shared.h"
#include "SkyCamera.h"
#include "ai_basenpc.h"
#include "modelentities.h"
#include "basetoggle.h"
#include "triggers.h"
#include "nav_area.h"
#include "AI_Criteria.h"
#include "saverestore.h"
#include "vcollide_parse.h"
#include "iservervehicle.h"
#include "gib.h"
#include "spark.h"
#include "filters.h"
#include "EntityFlame.h"
#include "player_resource.h"
#include "props.h"
#include "physics_prop_ragdoll.h"
#include "tier0/valve_minmax_off.h"
#include "srcpy.h"
#include "tier0/valve_minmax_on.h"
#include "tier0/memdbgon.h"
#include "CBaseToggle_pypp.hpp"

namespace bp = boost::python;

struct CBaseToggle_wrapper : CBaseToggle, bp::wrapper< CBaseToggle > {

    CBaseToggle_wrapper( )
    : CBaseToggle( )
      , bp::wrapper< CBaseToggle >(){
        // null constructor
    
    }

    virtual bool KeyValue( char const * szKeyName, char const * szValue ) {
        PY_OVERRIDE_CHECK( CBaseToggle, KeyValue )
        PY_OVERRIDE_LOG( _entities, CBaseToggle, KeyValue )
        bp::override func_KeyValue = this->get_override( "KeyValue" );
        if( func_KeyValue.ptr() != Py_None )
            try {
                return func_KeyValue( szKeyName, szValue );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseToggle::KeyValue( szKeyName, szValue );
            }
        else
            return this->CBaseToggle::KeyValue( szKeyName, szValue );
    }
    
    bool default_KeyValue( char const * szKeyName, char const * szValue ) {
        return CBaseToggle::KeyValue( szKeyName, szValue );
    }

    virtual bool KeyValue( char const * szKeyName, ::Vector vec ) {
        PY_OVERRIDE_CHECK( CBaseToggle, KeyValue )
        PY_OVERRIDE_LOG( _entities, CBaseToggle, KeyValue )
        bp::override func_KeyValue = this->get_override( "KeyValue" );
        if( func_KeyValue.ptr() != Py_None )
            try {
                return func_KeyValue( szKeyName, vec );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseToggle::KeyValue( szKeyName, vec );
            }
        else
            return this->CBaseToggle::KeyValue( szKeyName, vec );
    }
    
    bool default_KeyValue( char const * szKeyName, ::Vector vec ) {
        return CBaseToggle::KeyValue( szKeyName, vec );
    }

    virtual bool KeyValue( char const * szKeyName, float flValue ) {
        PY_OVERRIDE_CHECK( CBaseToggle, KeyValue )
        PY_OVERRIDE_LOG( _entities, CBaseToggle, KeyValue )
        bp::override func_KeyValue = this->get_override( "KeyValue" );
        if( func_KeyValue.ptr() != Py_None )
            try {
                return func_KeyValue( szKeyName, flValue );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseToggle::KeyValue( szKeyName, flValue );
            }
        else
            return this->CBaseToggle::KeyValue( szKeyName, flValue );
    }
    
    bool default_KeyValue( char const * szKeyName, float flValue ) {
        return CBaseToggle::KeyValue( szKeyName, flValue );
    }

    virtual void Activate(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, Activate )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, Activate )
        bp::override func_Activate = this->get_override( "Activate" );
        if( func_Activate.ptr() != Py_None )
            try {
                func_Activate(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::Activate(  );
            }
        else
            this->CBaseEntity::Activate(  );
    }
    
    void default_Activate(  ) {
        CBaseEntity::Activate( );
    }

    virtual void ComputeWorldSpaceSurroundingBox( ::Vector * pWorldMins, ::Vector * pWorldMaxs ) {
        PY_OVERRIDE_CHECK( CBaseEntity, ComputeWorldSpaceSurroundingBox )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, ComputeWorldSpaceSurroundingBox )
        bp::override func_ComputeWorldSpaceSurroundingBox = this->get_override( "ComputeWorldSpaceSurroundingBox" );
        if( func_ComputeWorldSpaceSurroundingBox.ptr() != Py_None )
            try {
                func_ComputeWorldSpaceSurroundingBox( boost::python::ptr(pWorldMins), boost::python::ptr(pWorldMaxs) );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::ComputeWorldSpaceSurroundingBox( pWorldMins, pWorldMaxs );
            }
        else
            this->CBaseEntity::ComputeWorldSpaceSurroundingBox( pWorldMins, pWorldMaxs );
    }
    
    void default_ComputeWorldSpaceSurroundingBox( ::Vector * pWorldMins, ::Vector * pWorldMaxs ) {
        CBaseEntity::ComputeWorldSpaceSurroundingBox( pWorldMins, pWorldMaxs );
    }

    virtual bool CreateVPhysics(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, CreateVPhysics )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, CreateVPhysics )
        bp::override func_CreateVPhysics = this->get_override( "CreateVPhysics" );
        if( func_CreateVPhysics.ptr() != Py_None )
            try {
                return func_CreateVPhysics(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseEntity::CreateVPhysics(  );
            }
        else
            return this->CBaseEntity::CreateVPhysics(  );
    }
    
    bool default_CreateVPhysics(  ) {
        return CBaseEntity::CreateVPhysics( );
    }

    virtual void DeathNotice( ::CBaseEntity * pVictim ) {
        PY_OVERRIDE_CHECK( CBaseEntity, DeathNotice )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, DeathNotice )
        bp::override func_DeathNotice = this->get_override( "DeathNotice" );
        if( func_DeathNotice.ptr() != Py_None )
            try {
                func_DeathNotice( pVictim ? pVictim->GetPyHandle() : boost::python::object() );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::DeathNotice( pVictim );
            }
        else
            this->CBaseEntity::DeathNotice( pVictim );
    }
    
    void default_DeathNotice( ::CBaseEntity * pVictim ) {
        CBaseEntity::DeathNotice( pVictim );
    }

    virtual void DoImpactEffect( ::trace_t & tr, int nDamageType ) {
        PY_OVERRIDE_CHECK( CBaseEntity, DoImpactEffect )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, DoImpactEffect )
        bp::override func_DoImpactEffect = this->get_override( "DoImpactEffect" );
        if( func_DoImpactEffect.ptr() != Py_None )
            try {
                func_DoImpactEffect( boost::ref(tr), nDamageType );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::DoImpactEffect( tr, nDamageType );
            }
        else
            this->CBaseEntity::DoImpactEffect( tr, nDamageType );
    }
    
    void default_DoImpactEffect( ::trace_t & tr, int nDamageType ) {
        CBaseEntity::DoImpactEffect( tr, nDamageType );
    }

    virtual void DrawDebugGeometryOverlays(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, DrawDebugGeometryOverlays )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, DrawDebugGeometryOverlays )
        bp::override func_DrawDebugGeometryOverlays = this->get_override( "DrawDebugGeometryOverlays" );
        if( func_DrawDebugGeometryOverlays.ptr() != Py_None )
            try {
                func_DrawDebugGeometryOverlays(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::DrawDebugGeometryOverlays(  );
            }
        else
            this->CBaseEntity::DrawDebugGeometryOverlays(  );
    }
    
    void default_DrawDebugGeometryOverlays(  ) {
        CBaseEntity::DrawDebugGeometryOverlays( );
    }

    virtual int DrawDebugTextOverlays(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, DrawDebugTextOverlays )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, DrawDebugTextOverlays )
        bp::override func_DrawDebugTextOverlays = this->get_override( "DrawDebugTextOverlays" );
        if( func_DrawDebugTextOverlays.ptr() != Py_None )
            try {
                return func_DrawDebugTextOverlays(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseEntity::DrawDebugTextOverlays(  );
            }
        else
            return this->CBaseEntity::DrawDebugTextOverlays(  );
    }
    
    int default_DrawDebugTextOverlays(  ) {
        return CBaseEntity::DrawDebugTextOverlays( );
    }

    virtual void EndTouch( ::CBaseEntity * pOther ) {
        PY_OVERRIDE_CHECK( CBaseEntity, EndTouch )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, EndTouch )
        bp::override func_EndTouch = this->get_override( "EndTouch" );
        if( func_EndTouch.ptr() != Py_None )
            try {
                func_EndTouch( pOther ? pOther->GetPyHandle() : boost::python::object() );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::EndTouch( pOther );
            }
        else
            this->CBaseEntity::EndTouch( pOther );
    }
    
    void default_EndTouch( ::CBaseEntity * pOther ) {
        CBaseEntity::EndTouch( pOther );
    }

    virtual void Event_Killed( ::CTakeDamageInfo const & info ) {
        PY_OVERRIDE_CHECK( CBaseEntity, Event_Killed )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, Event_Killed )
        bp::override func_Event_Killed = this->get_override( "Event_Killed" );
        if( func_Event_Killed.ptr() != Py_None )
            try {
                func_Event_Killed( boost::ref(info) );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::Event_Killed( info );
            }
        else
            this->CBaseEntity::Event_Killed( info );
    }
    
    void default_Event_Killed( ::CTakeDamageInfo const & info ) {
        CBaseEntity::Event_Killed( info );
    }

    virtual char const * GetTracerType(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, GetTracerType )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, GetTracerType )
        bp::override func_GetTracerType = this->get_override( "GetTracerType" );
        if( func_GetTracerType.ptr() != Py_None )
            try {
                return func_GetTracerType(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseEntity::GetTracerType(  );
            }
        else
            return this->CBaseEntity::GetTracerType(  );
    }
    
    char const * default_GetTracerType(  ) {
        return CBaseEntity::GetTracerType( );
    }

    virtual bool KeyValue( char const * szKeyName, ::Vector const & vecValue ) {
        PY_OVERRIDE_CHECK( CBaseEntity, KeyValue )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, KeyValue )
        bp::override func_KeyValue = this->get_override( "KeyValue" );
        if( func_KeyValue.ptr() != Py_None )
            try {
                return func_KeyValue( szKeyName, boost::ref(vecValue) );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseEntity::KeyValue( szKeyName, vecValue );
            }
        else
            return this->CBaseEntity::KeyValue( szKeyName, vecValue );
    }
    
    bool default_KeyValue( char const * szKeyName, ::Vector const & vecValue ) {
        return CBaseEntity::KeyValue( szKeyName, vecValue );
    }

    virtual void MakeTracer( ::Vector const & vecTracerSrc, ::trace_t const & tr, int iTracerType ) {
        PY_OVERRIDE_CHECK( CBaseEntity, MakeTracer )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, MakeTracer )
        bp::override func_MakeTracer = this->get_override( "MakeTracer" );
        if( func_MakeTracer.ptr() != Py_None )
            try {
                func_MakeTracer( boost::ref(vecTracerSrc), boost::ref(tr), iTracerType );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::MakeTracer( vecTracerSrc, tr, iTracerType );
            }
        else
            this->CBaseEntity::MakeTracer( vecTracerSrc, tr, iTracerType );
    }
    
    void default_MakeTracer( ::Vector const & vecTracerSrc, ::trace_t const & tr, int iTracerType ) {
        CBaseEntity::MakeTracer( vecTracerSrc, tr, iTracerType );
    }

    virtual void ModifyOrAppendCriteria( ::AI_CriteriaSet & set ) {
        PY_OVERRIDE_CHECK( CBaseEntity, ModifyOrAppendCriteria )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, ModifyOrAppendCriteria )
        bp::override func_ModifyOrAppendCriteria = this->get_override( "ModifyOrAppendCriteria" );
        if( func_ModifyOrAppendCriteria.ptr() != Py_None )
            try {
                func_ModifyOrAppendCriteria( boost::ref(set) );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::ModifyOrAppendCriteria( set );
            }
        else
            this->CBaseEntity::ModifyOrAppendCriteria( set );
    }
    
    void default_ModifyOrAppendCriteria( ::AI_CriteriaSet & set ) {
        CBaseEntity::ModifyOrAppendCriteria( set );
    }

    virtual void OnRestore(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, OnRestore )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, OnRestore )
        bp::override func_OnRestore = this->get_override( "OnRestore" );
        if( func_OnRestore.ptr() != Py_None )
            try {
                func_OnRestore(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::OnRestore(  );
            }
        else
            this->CBaseEntity::OnRestore(  );
    }
    
    void default_OnRestore(  ) {
        CBaseEntity::OnRestore( );
    }

    virtual int OnTakeDamage( ::CTakeDamageInfo const & info ) {
        PY_OVERRIDE_CHECK( CBaseEntity, OnTakeDamage )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, OnTakeDamage )
        bp::override func_OnTakeDamage = this->get_override( "OnTakeDamage" );
        if( func_OnTakeDamage.ptr() != Py_None )
            try {
                return func_OnTakeDamage( boost::ref(info) );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseEntity::OnTakeDamage( info );
            }
        else
            return this->CBaseEntity::OnTakeDamage( info );
    }
    
    int default_OnTakeDamage( ::CTakeDamageInfo const & info ) {
        return CBaseEntity::OnTakeDamage( info );
    }

    virtual bool PassesDamageFilter( ::CTakeDamageInfo const & info ) {
        PY_OVERRIDE_CHECK( CBaseEntity, PassesDamageFilter )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, PassesDamageFilter )
        bp::override func_PassesDamageFilter = this->get_override( "PassesDamageFilter" );
        if( func_PassesDamageFilter.ptr() != Py_None )
            try {
                return func_PassesDamageFilter( boost::ref(info) );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseEntity::PassesDamageFilter( info );
            }
        else
            return this->CBaseEntity::PassesDamageFilter( info );
    }
    
    bool default_PassesDamageFilter( ::CTakeDamageInfo const & info ) {
        return CBaseEntity::PassesDamageFilter( info );
    }

    virtual void PostClientActive(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, PostClientActive )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, PostClientActive )
        bp::override func_PostClientActive = this->get_override( "PostClientActive" );
        if( func_PostClientActive.ptr() != Py_None )
            try {
                func_PostClientActive(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::PostClientActive(  );
            }
        else
            this->CBaseEntity::PostClientActive(  );
    }
    
    void default_PostClientActive(  ) {
        CBaseEntity::PostClientActive( );
    }

    virtual void PostConstructor( char const * szClassname ) {
        PY_OVERRIDE_CHECK( CBaseEntity, PostConstructor )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, PostConstructor )
        bp::override func_PostConstructor = this->get_override( "PostConstructor" );
        if( func_PostConstructor.ptr() != Py_None )
            try {
                func_PostConstructor( szClassname );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::PostConstructor( szClassname );
            }
        else
            this->CBaseEntity::PostConstructor( szClassname );
    }
    
    void default_PostConstructor( char const * szClassname ) {
        CBaseEntity::PostConstructor( szClassname );
    }

    virtual void Precache(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, Precache )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, Precache )
        bp::override func_Precache = this->get_override( "Precache" );
        if( func_Precache.ptr() != Py_None )
            try {
                func_Precache(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::Precache(  );
            }
        else
            this->CBaseEntity::Precache(  );
    }
    
    void default_Precache(  ) {
        CBaseEntity::Precache( );
    }

    virtual void Spawn(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, Spawn )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, Spawn )
        bp::override func_Spawn = this->get_override( "Spawn" );
        if( func_Spawn.ptr() != Py_None )
            try {
                func_Spawn(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::Spawn(  );
            }
        else
            this->CBaseEntity::Spawn(  );
    }
    
    void default_Spawn(  ) {
        CBaseEntity::Spawn( );
    }

    virtual void StartTouch( ::CBaseEntity * pOther ) {
        PY_OVERRIDE_CHECK( CBaseEntity, StartTouch )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, StartTouch )
        bp::override func_StartTouch = this->get_override( "StartTouch" );
        if( func_StartTouch.ptr() != Py_None )
            try {
                func_StartTouch( pOther ? pOther->GetPyHandle() : boost::python::object() );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::StartTouch( pOther );
            }
        else
            this->CBaseEntity::StartTouch( pOther );
    }
    
    void default_StartTouch( ::CBaseEntity * pOther ) {
        CBaseEntity::StartTouch( pOther );
    }

    virtual void StopLoopingSounds(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, StopLoopingSounds )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, StopLoopingSounds )
        bp::override func_StopLoopingSounds = this->get_override( "StopLoopingSounds" );
        if( func_StopLoopingSounds.ptr() != Py_None )
            try {
                func_StopLoopingSounds(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::StopLoopingSounds(  );
            }
        else
            this->CBaseEntity::StopLoopingSounds(  );
    }
    
    void default_StopLoopingSounds(  ) {
        CBaseEntity::StopLoopingSounds( );
    }

    void TraceAttack( ::CTakeDamageInfo const & info, ::Vector const & vecDir, ::trace_t * ptr, ::CDmgAccumulator * pAccumulator=0 ){
        CBaseEntity::TraceAttack( info, vecDir, ptr, pAccumulator );
    }

    virtual void UpdateOnRemove(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, UpdateOnRemove )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, UpdateOnRemove )
        bp::override func_UpdateOnRemove = this->get_override( "UpdateOnRemove" );
        if( func_UpdateOnRemove.ptr() != Py_None )
            try {
                func_UpdateOnRemove(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::UpdateOnRemove(  );
            }
        else
            this->CBaseEntity::UpdateOnRemove(  );
    }
    
    void default_UpdateOnRemove(  ) {
        CBaseEntity::UpdateOnRemove( );
    }

    virtual int UpdateTransmitState(  ) {
        PY_OVERRIDE_CHECK( CBaseEntity, UpdateTransmitState )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, UpdateTransmitState )
        bp::override func_UpdateTransmitState = this->get_override( "UpdateTransmitState" );
        if( func_UpdateTransmitState.ptr() != Py_None )
            try {
                return func_UpdateTransmitState(  );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                return this->CBaseEntity::UpdateTransmitState(  );
            }
        else
            return this->CBaseEntity::UpdateTransmitState(  );
    }
    
    int default_UpdateTransmitState(  ) {
        return CBaseEntity::UpdateTransmitState( );
    }

    virtual void VPhysicsCollision( int index, ::gamevcollisionevent_t * pEvent ) {
        PY_OVERRIDE_CHECK( CBaseEntity, VPhysicsCollision )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, VPhysicsCollision )
        bp::override func_VPhysicsCollision = this->get_override( "VPhysicsCollision" );
        if( func_VPhysicsCollision.ptr() != Py_None )
            try {
                func_VPhysicsCollision( index, boost::python::ptr(pEvent) );
            } catch(bp::error_already_set &) {
                PyErr_Print();
                this->CBaseEntity::VPhysicsCollision( index, pEvent );
            }
        else
            this->CBaseEntity::VPhysicsCollision( index, pEvent );
    }
    
    void default_VPhysicsCollision( int index, ::gamevcollisionevent_t * pEvent ) {
        CBaseEntity::VPhysicsCollision( index, pEvent );
    }

    virtual PyObject *GetPySelf() const { return bp::detail::wrapper_base_::get_owner(*this); }

    virtual ServerClass* GetServerClass() {
        PY_OVERRIDE_CHECK( CBaseEntity, GetServerClass )
        PY_OVERRIDE_LOG( _entities, CBaseEntity, GetServerClass )
        ServerClass *pServerClass = SrcPySystem()->Get<ServerClass *>( "pyServerClass", GetPyInstance(), NULL, true );
        if( pServerClass )
            return pServerClass;
        return CBaseEntity::GetServerClass();
    }

    static int m_lifeState_Get( CBaseToggle const & inst ) { return inst.m_lifeState.Get(); }

    static void m_lifeState_Set( CBaseToggle & inst, int val ) { inst.m_lifeState.Set( val ); }

    static int m_takedamage_Get( CBaseToggle const & inst ) { return inst.m_takedamage.Get(); }

    static void m_takedamage_Set( CBaseToggle & inst, int val ) { inst.m_takedamage.Set( val ); }

};

void register_CBaseToggle_class(){

    bp::class_< CBaseToggle_wrapper, bp::bases< CBaseEntity >, boost::noncopyable >( "CBaseToggle", bp::init< >() )    
        .def( 
            "AngularMove"
            , (void ( ::CBaseToggle::* )( ::QAngle const &,float ) )( &::CBaseToggle::AngularMove )
            , ( bp::arg("vecDestAngle"), bp::arg("flSpeed") ) )    
        .def( 
            "AngularMoveDone"
            , (void ( ::CBaseToggle::* )(  ) )( &::CBaseToggle::AngularMoveDone ) )    
        .def( 
            "AxisDelta"
            , (float (*)( int,::QAngle const &,::QAngle const & ))( &::CBaseToggle::AxisDelta )
            , ( bp::arg("flags"), bp::arg("angle1"), bp::arg("angle2") ) )    
        .def( 
            "AxisDir"
            , (void ( ::CBaseToggle::* )(  ) )( &::CBaseToggle::AxisDir ) )    
        .def( 
            "AxisValue"
            , (float (*)( int,::QAngle const & ))( &::CBaseToggle::AxisValue )
            , ( bp::arg("flags"), bp::arg("angles") ) )    
        .def( 
            "GetDelay"
            , (float ( ::CBaseToggle::* )(  ) )( &::CBaseToggle::GetDelay ) )    
        .def( 
            "IsLockedByMaster"
            , (bool ( ::CBaseToggle::* )(  ) )( &::CBaseToggle::IsLockedByMaster ) )    
        .def( 
            "KeyValue"
            , (bool ( ::CBaseToggle::* )( char const *,char const * ) )(&::CBaseToggle::KeyValue)
            , (bool ( CBaseToggle_wrapper::* )( char const *,char const * ) )(&CBaseToggle_wrapper::default_KeyValue)
            , ( bp::arg("szKeyName"), bp::arg("szValue") ) )    
        .def( 
            "KeyValue"
            , (bool ( ::CBaseToggle::* )( char const *,::Vector ) )(&::CBaseToggle::KeyValue)
            , (bool ( CBaseToggle_wrapper::* )( char const *,::Vector ) )(&CBaseToggle_wrapper::default_KeyValue)
            , ( bp::arg("szKeyName"), bp::arg("vec") ) )    
        .def( 
            "KeyValue"
            , (bool ( ::CBaseToggle::* )( char const *,float ) )(&::CBaseToggle::KeyValue)
            , (bool ( CBaseToggle_wrapper::* )( char const *,float ) )(&CBaseToggle_wrapper::default_KeyValue)
            , ( bp::arg("szKeyName"), bp::arg("flValue") ) )    
        .def( 
            "LinearMove"
            , (void ( ::CBaseToggle::* )( ::Vector const &,float ) )( &::CBaseToggle::LinearMove )
            , ( bp::arg("vecDest"), bp::arg("flSpeed") ) )    
        .def( 
            "LinearMoveDone"
            , (void ( ::CBaseToggle::* )(  ) )( &::CBaseToggle::LinearMoveDone ) )    
        .def( 
            "MoveDone"
            , (void ( ::CBaseToggle::* )(  ) )( &::CBaseToggle::MoveDone ) )    
        .def( 
            "Activate"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::Activate)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_Activate) )    
        .def( 
            "ComputeWorldSpaceSurroundingBox"
            , (void ( ::CBaseEntity::* )( ::Vector *,::Vector * ) )(&::CBaseEntity::ComputeWorldSpaceSurroundingBox)
            , (void ( CBaseToggle_wrapper::* )( ::Vector *,::Vector * ) )(&CBaseToggle_wrapper::default_ComputeWorldSpaceSurroundingBox)
            , ( bp::arg("pWorldMins"), bp::arg("pWorldMaxs") ) )    
        .def( 
            "CreateVPhysics"
            , (bool ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::CreateVPhysics)
            , (bool ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_CreateVPhysics) )    
        .def( 
            "DeathNotice"
            , (void ( ::CBaseEntity::* )( ::CBaseEntity * ) )(&::CBaseEntity::DeathNotice)
            , (void ( CBaseToggle_wrapper::* )( ::CBaseEntity * ) )(&CBaseToggle_wrapper::default_DeathNotice)
            , ( bp::arg("pVictim") ) )    
        .def( 
            "DoImpactEffect"
            , (void ( ::CBaseEntity::* )( ::trace_t &,int ) )(&::CBaseEntity::DoImpactEffect)
            , (void ( CBaseToggle_wrapper::* )( ::trace_t &,int ) )(&CBaseToggle_wrapper::default_DoImpactEffect)
            , ( bp::arg("tr"), bp::arg("nDamageType") ) )    
        .def( 
            "DrawDebugGeometryOverlays"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::DrawDebugGeometryOverlays)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_DrawDebugGeometryOverlays) )    
        .def( 
            "DrawDebugTextOverlays"
            , (int ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::DrawDebugTextOverlays)
            , (int ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_DrawDebugTextOverlays) )    
        .def( 
            "EndTouch"
            , (void ( ::CBaseEntity::* )( ::CBaseEntity * ) )(&::CBaseEntity::EndTouch)
            , (void ( CBaseToggle_wrapper::* )( ::CBaseEntity * ) )(&CBaseToggle_wrapper::default_EndTouch)
            , ( bp::arg("pOther") ) )    
        .def( 
            "Event_Killed"
            , (void ( ::CBaseEntity::* )( ::CTakeDamageInfo const & ) )(&::CBaseEntity::Event_Killed)
            , (void ( CBaseToggle_wrapper::* )( ::CTakeDamageInfo const & ) )(&CBaseToggle_wrapper::default_Event_Killed)
            , ( bp::arg("info") ) )    
        .def( 
            "GetTracerType"
            , (char const * ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::GetTracerType)
            , (char const * ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_GetTracerType) )    
        .def( 
            "KeyValue"
            , (bool ( ::CBaseEntity::* )( char const *,::Vector const & ) )(&::CBaseEntity::KeyValue)
            , (bool ( CBaseToggle_wrapper::* )( char const *,::Vector const & ) )(&CBaseToggle_wrapper::default_KeyValue)
            , ( bp::arg("szKeyName"), bp::arg("vecValue") ) )    
        .def( 
            "MakeTracer"
            , (void ( ::CBaseEntity::* )( ::Vector const &,::trace_t const &,int ) )(&::CBaseEntity::MakeTracer)
            , (void ( CBaseToggle_wrapper::* )( ::Vector const &,::trace_t const &,int ) )(&CBaseToggle_wrapper::default_MakeTracer)
            , ( bp::arg("vecTracerSrc"), bp::arg("tr"), bp::arg("iTracerType") ) )    
        .def( 
            "ModifyOrAppendCriteria"
            , (void ( ::CBaseEntity::* )( ::AI_CriteriaSet & ) )(&::CBaseEntity::ModifyOrAppendCriteria)
            , (void ( CBaseToggle_wrapper::* )( ::AI_CriteriaSet & ) )(&CBaseToggle_wrapper::default_ModifyOrAppendCriteria)
            , ( bp::arg("set") ) )    
        .def( 
            "OnRestore"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::OnRestore)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_OnRestore) )    
        .def( 
            "OnTakeDamage"
            , (int ( ::CBaseEntity::* )( ::CTakeDamageInfo const & ) )(&::CBaseEntity::OnTakeDamage)
            , (int ( CBaseToggle_wrapper::* )( ::CTakeDamageInfo const & ) )(&CBaseToggle_wrapper::default_OnTakeDamage)
            , ( bp::arg("info") ) )    
        .def( 
            "PassesDamageFilter"
            , (bool ( ::CBaseEntity::* )( ::CTakeDamageInfo const & ) )(&::CBaseEntity::PassesDamageFilter)
            , (bool ( CBaseToggle_wrapper::* )( ::CTakeDamageInfo const & ) )(&CBaseToggle_wrapper::default_PassesDamageFilter)
            , ( bp::arg("info") ) )    
        .def( 
            "PostClientActive"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::PostClientActive)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_PostClientActive) )    
        .def( 
            "PostConstructor"
            , (void ( ::CBaseEntity::* )( char const * ) )(&::CBaseEntity::PostConstructor)
            , (void ( CBaseToggle_wrapper::* )( char const * ) )(&CBaseToggle_wrapper::default_PostConstructor)
            , ( bp::arg("szClassname") ) )    
        .def( 
            "Precache"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::Precache)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_Precache) )    
        .def( 
            "Spawn"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::Spawn)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_Spawn) )    
        .def( 
            "StartTouch"
            , (void ( ::CBaseEntity::* )( ::CBaseEntity * ) )(&::CBaseEntity::StartTouch)
            , (void ( CBaseToggle_wrapper::* )( ::CBaseEntity * ) )(&CBaseToggle_wrapper::default_StartTouch)
            , ( bp::arg("pOther") ) )    
        .def( 
            "StopLoopingSounds"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::StopLoopingSounds)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_StopLoopingSounds) )    
        .def( 
            "TraceAttack"
            , (void ( CBaseToggle_wrapper::* )( ::CTakeDamageInfo const &,::Vector const &,::trace_t *,::CDmgAccumulator * ) )(&CBaseToggle_wrapper::TraceAttack)
            , ( bp::arg("info"), bp::arg("vecDir"), bp::arg("ptr"), bp::arg("pAccumulator")=bp::object() ) )    
        .def( 
            "UpdateOnRemove"
            , (void ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::UpdateOnRemove)
            , (void ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_UpdateOnRemove) )    
        .def( 
            "UpdateTransmitState"
            , (int ( ::CBaseEntity::* )(  ) )(&::CBaseEntity::UpdateTransmitState)
            , (int ( CBaseToggle_wrapper::* )(  ) )(&CBaseToggle_wrapper::default_UpdateTransmitState) )    
        .def( 
            "VPhysicsCollision"
            , (void ( ::CBaseEntity::* )( int,::gamevcollisionevent_t * ) )(&::CBaseEntity::VPhysicsCollision)
            , (void ( CBaseToggle_wrapper::* )( int,::gamevcollisionevent_t * ) )(&CBaseToggle_wrapper::default_VPhysicsCollision)
            , ( bp::arg("index"), bp::arg("pEvent") ) )    
        .staticmethod( "AxisDelta" )    
        .staticmethod( "AxisValue" )    
        .add_property( "lifestate", &CBaseToggle_wrapper::m_lifeState_Get, &CBaseToggle_wrapper::m_lifeState_Set )    
        .add_property( "takedamage", &CBaseToggle_wrapper::m_takedamage_Get, &CBaseToggle_wrapper::m_takedamage_Set );

}

