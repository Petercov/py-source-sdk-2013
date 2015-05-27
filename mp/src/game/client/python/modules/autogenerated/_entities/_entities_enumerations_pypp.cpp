// This file has been generated by Py++.

#include "cbase.h"
// This file has been generated by Py++.

#include "cbase.h"
#include "npcevent.h"
#include "srcpy_entities.h"
#include "bone_setup.h"
#include "baseprojectile.h"
#include "basegrenade_shared.h"
#include "takedamageinfo.h"
#include "c_ai_basenpc.h"
#include "soundinfo.h"
#include "saverestore.h"
#include "saverestoretypes.h"
#include "vcollide_parse.h"
#include "iclientvehicle.h"
#include "steam/steamclientpublic.h"
#include "view_shared.h"
#include "c_playerresource.h"
#include "c_breakableprop.h"
#include "tier0/valve_minmax_off.h"
#include "srcpy.h"
#include "tier0/valve_minmax_on.h"
#include "tier0/memdbgon.h"
#include "_entities_enumerations_pypp.hpp"

namespace bp = boost::python;

void _entities_register_enumerations(){

    bp::enum_< MoveCollide_t>("MoveCollide_t")
        .value("MOVECOLLIDE_DEFAULT", MOVECOLLIDE_DEFAULT)
        .value("MOVECOLLIDE_FLY_BOUNCE", MOVECOLLIDE_FLY_BOUNCE)
        .value("MOVECOLLIDE_FLY_CUSTOM", MOVECOLLIDE_FLY_CUSTOM)
        .value("MOVECOLLIDE_FLY_SLIDE", MOVECOLLIDE_FLY_SLIDE)
        .value("MOVECOLLIDE_COUNT", MOVECOLLIDE_COUNT)
        .value("MOVECOLLIDE_MAX_BITS", MOVECOLLIDE_MAX_BITS)
        .export_values()
        ;

    bp::enum_< WeaponSound_t>("WeaponSound")
        .value("EMPTY", EMPTY)
        .value("SINGLE", SINGLE)
        .value("SINGLE_NPC", SINGLE_NPC)
        .value("WPN_DOUBLE", WPN_DOUBLE)
        .value("DOUBLE_NPC", DOUBLE_NPC)
        .value("BURST", BURST)
        .value("RELOAD", RELOAD)
        .value("RELOAD_NPC", RELOAD_NPC)
        .value("MELEE_MISS", MELEE_MISS)
        .value("MELEE_HIT", MELEE_HIT)
        .value("MELEE_HIT_WORLD", MELEE_HIT_WORLD)
        .value("SPECIAL1", SPECIAL1)
        .value("SPECIAL2", SPECIAL2)
        .value("SPECIAL3", SPECIAL3)
        .value("TAUNT", TAUNT)
        .value("DEPLOY", DEPLOY)
        .value("NUM_SHOOT_SOUND_TYPES", NUM_SHOOT_SOUND_TYPES)
        .export_values()
        ;

}

