## PySource
A Source SDK 2013 fork with automatically generated bindings for Python 3. 
The aim of these bindings is to have a (semi) safe Python environment of Source Engine.
For a better idea of what these bindings offer, check out the [examples](mp/game/pysource/python/examples) directory.

These automatic bindings were originally made for [Half-Life 2: Wars](https://github.com/Sandern/hl2wars_asw_dev) mod, which
uses Python 2. Also see the [Python folder](http://svn.hl2wars.com/hl2wars_asw_dev/trunk/python/) of this for more examples 
of what ispossible (most game code of the mod is written in Python!).

This Source SDK 2013 version is a cleaned up port of these auto generated bindings to Python 3. Due this, some things
might still be missing or are incomplete and will be added in time.

Please let me know if you have any issues. Pull requests are welcome too!

## Quickstart
Currently Windows only:

1. Run [mp/src/createpysourceprojects.bat](mp/src/createpysourceprojects.bat) 
2. Open games.sln and compile
3. Start mp/game/PySource and load a map
4. Test Python by entering one of the following commands:

        spy print('Hello Source')

        spy print(UTIL_PlayerByIndex(1).GetPlayerName())

## Examples
Examples can be found in the Python game directory [examples](mp/game/pysource/python/examples). 
These examples cover the [Your First Entity](https://developer.valvesoftware.com/wiki/Your_First_Entity) page from VDC among others.

## Commands

        spy - Evaluates a Python string on the server

        cpy - Evaluates a Python string on the client

## Generating new modules
PySource makes use of gccxml, pygccxml and pyplusplus to generate Boost Python bindings.
You can find instructions in [mp/src/srcpypp](mp/src/srcpypp).

## List of binding modules
- [srcbuiltins](mp/src/game/shared/python/modules/srcbuiltins.py): Exposes debug Msg functions, used for redirecting output of Python
- [_vmath](mp/src/game/shared/python/modules/_vmath.py): Exposes mathlib
- [_entities](mp/src/game/shared/python/modules/_entities.py): Exposes most base entity classes (CBaseEntity, CBaseAnimating, etc)
- [_entitiesmisc](mp/src/game/shared/python/modules/_entitiesmisc.py): Exposes miscellaneous bindings related to entities, like the entity list
- [_physics](mp/src/game/shared/python/modules/_physics.py): Exposed Particle system related functions, like DispatchParticleEffect.
- [_gameinterface](mp/src/game/shared/python/modules/_gameinterface.py): Exposes game engine interface, user messages, ConCommands and ConVars among others.
- [_utils](mp/src/game/shared/python/modules/_utils.py): Exposes utils functions and related (e.g. UTIL_TraceLine)
- [_sound](mp/src/game/shared/python/modules/_sound.py): Exposes sound engine interface and related.
- [_animation](mp/src/game/shared/python/modules/_animation.py): Exposed functions from - [animation.h](mp/src/game/shared/animation.h)
- [_ndebugoverlay](mp/src/game/shared/python/modules/_ndebugoverlay.py): Exposes [NDebugOverlay](mp/src/game/shared/debugoverlay_shared.h) functions.
- [vprof](mp/src/game/shared/python/modules/vprof.py): Exposes VProfiling

Note: Most of these modules are complemented by [Python modules](mp/game/pysource/python) (e.g. [entities](mp/game/pysource/python/entities.py))