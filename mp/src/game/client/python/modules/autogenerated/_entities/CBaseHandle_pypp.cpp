// This file has been generated by Py++.

#include "cbase.h"
// This file has been generated by Py++.

#include "cbase.h"
#include "npcevent.h"
#include "srcpy_entities.h"
#include "bone_setup.h"
#include "basegrenade_shared.h"
#include "takedamageinfo.h"
#include "c_ai_basenpc.h"
#include "soundinfo.h"
#include "isaverestore.h"
#include "tier0/valve_minmax_off.h"
#include "srcpy.h"
#include "tier0/valve_minmax_on.h"
#include "tier0/memdbgon.h"
#include "CBaseHandle_pypp.hpp"

namespace bp = boost::python;

void register_CBaseHandle_class(){

    { //::CBaseHandle
        typedef bp::class_< CBaseHandle > CBaseHandle_exposer_t;
        CBaseHandle_exposer_t CBaseHandle_exposer = CBaseHandle_exposer_t( "CBaseHandle", bp::init< >() );
        bp::scope CBaseHandle_scope( CBaseHandle_exposer );
        CBaseHandle_exposer.def( bp::init< CBaseHandle const & >(( bp::arg("other") )) );
        CBaseHandle_exposer.def( bp::init< long unsigned int >(( bp::arg("value") )) );
        bp::implicitly_convertible< long unsigned int, CBaseHandle >();
        CBaseHandle_exposer.def( bp::init< int, int >(( bp::arg("iEntry"), bp::arg("iSerialNumber") )) );
        { //::CBaseHandle::GetEntryIndex
        
            typedef int ( ::CBaseHandle::*GetEntryIndex_function_type )(  ) const;
            
            CBaseHandle_exposer.def( 
                "GetEntryIndex"
                , GetEntryIndex_function_type( &::CBaseHandle::GetEntryIndex ) );
        
        }
        { //::CBaseHandle::GetSerialNumber
        
            typedef int ( ::CBaseHandle::*GetSerialNumber_function_type )(  ) const;
            
            CBaseHandle_exposer.def( 
                "GetSerialNumber"
                , GetSerialNumber_function_type( &::CBaseHandle::GetSerialNumber ) );
        
        }
        { //::CBaseHandle::IsValid
        
            typedef bool ( ::CBaseHandle::*IsValid_function_type )(  ) const;
            
            CBaseHandle_exposer.def( 
                "IsValid"
                , IsValid_function_type( &::CBaseHandle::IsValid ) );
        
        }
        { //::CBaseHandle::ToInt
        
            typedef int ( ::CBaseHandle::*ToInt_function_type )(  ) const;
            
            CBaseHandle_exposer.def( 
                "ToInt"
                , ToInt_function_type( &::CBaseHandle::ToInt ) );
        
        }
        CBaseHandle_exposer.def( bp::self != bp::self );
        CBaseHandle_exposer.def( bp::self != bp::other< IHandleEntity const * >() );
        CBaseHandle_exposer.def( bp::self < bp::self );
        CBaseHandle_exposer.def( bp::self < bp::other< IHandleEntity const * >() );
        { //::CBaseHandle::operator=
        
            typedef ::CBaseHandle const & ( ::CBaseHandle::*assign_function_type )( ::IHandleEntity const * ) ;
            
            CBaseHandle_exposer.def( 
                "assign"
                , assign_function_type( &::CBaseHandle::operator= )
                , ( bp::arg("pEntity") )
                , bp::return_value_policy< bp::copy_const_reference >() );
        
        }
        CBaseHandle_exposer.def( bp::self == bp::self );
        CBaseHandle_exposer.def( bp::self == bp::other< IHandleEntity const * >() );
    }

}

