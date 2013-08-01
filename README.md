## PySource
A Source SDK 2013 fork with automatically generated bindings for Python 3.

## Quickstart
Currently Windows only:
1. Run [mp/src/createpysourceprojects.bat](mp/src/createpysourceprojects.bat) 
2. Open games.sln and compile
3. Start mp/game/PySource and load a map
4. Test Python by entering the command "spy print('Hello Source')" or "spy print(UTIL_PlayerByIndex(1).GetPlayerName())"

## Examples
Examples can be found in game directory "[mp/game/PySource/python/examples](mp/game/PySource/python/examples)" (WIP)

## Commands
- spy - Evaluates a Python string on the server
- cpy - Evaluates a Python string on the client

## Generating new modules
PySource makes use of gccxml, pygccxml and pyplusplus to generate Boost Python bindings.
You can find instructions in [mp/src/srcpypp](mp/src/srcpypp).

## List of modules
- [srcbuiltins]([mp/src/game/shared/modules/srcbuiltins.py): Exposes debug Msg functions, used for redirecting output of Python
- [_vmath]([mp/src/game/shared/modules/_vmath.py): Exposes mathlib
- [_entities]([mp/src/game/shared/modules/entities.py): Exposes most base entity classes (CBaseEntity, CBaseAnimating, etc)
- [_entitiesmisc]([mp/src/game/shared/modules/_entitiesmisc.py): Exposes miscellaneous bindings related to entities, like the entity list
- [_physics]([mp/src/game/shared/modules/_physics.py): Exposed Particle system related functions, like DispatchParticleEffect.
- [_gameinterface]([mp/src/game/shared/modules/_gameinterface.py): Exposes game engine interface, user messages, ConCommands and ConVars among others.
- [_utils]([mp/src/game/shared/modules/_utils.py): Exposes utils functions and related (e.g. UTIL_TraceLine)
- [_sound]([mp/src/game/shared/modules/_sound.py): Exposes sound engine interface and related.
- [_animation]([mp/src/game/shared/modules/_animation.py): Exposed functions from - [animation.h]([mp/src/game/shared/animation.h)
- [_ndebugoverlay]([mp/src/game/shared/modules/_ndebugoverlay.py): Exposes [NDebugOverlay](mp/src/game/shared/debugoverlay_shared.h_) functions.
- [vprof]([mp/src/game/shared/modules/vprof.py): Exposes VProfiling