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
#include "IClientEntity_pypp.hpp"

namespace bp = boost::python;

void register_IClientEntity_class(){

    bp::class_< IClientEntity, bp::bases< IClientUnknown >, boost::noncopyable >( "IClientEntity", bp::no_init );

}

