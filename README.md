## PySource
A Source SDK 2013 fork with automatically generated bindings for Python 3. 
The aim of these bindings is to have a (semi) safe Python environment of Source Engine.
For a better idea of what these bindings offer, check out the [examples](mp/game/pysource/python/examples) directory.

These automatic bindings were originally made for [Half-Life 2: Wars](https://github.com/Sandern/hl2wars_asw_dev) mod, which
uses Python 2. Also see the [Python folder](http://svn.hl2wars.com/hl2wars_asw_dev/trunk/python/) of this for more examples 
of what is possible (most game code of the mod is written in Python!).

This Source SDK 2013 version is a cleaned up port of these auto generated bindings to Python 3. Due this, some things
might still be missing or are incomplete and will be added in time.

Please let me know if you have any issues. Pull requests are welcome too!

## Quickstart
Currently tested on Windows and OSX only:

1. Run [mp/src/createpysourceprojects](mp/src/createpysourceprojects) 
2. Open games.sln or games.xproj and compile
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

## Visual Studio Python Tools support (Experimental)
To allow easier debugging, Visual Studio Python Tools is supported. 
This includes Intellisense and setting breakpoints in Python code.

You can download VSPT from:

        http://pytools.codeplex.com/

To use VSPT, you must first add a new Python Environment:

1. Open [Python.sln](mp/game/pysource/python/python.sln)
2. Go to "Tools -> Options"
3. Go to "Python Tools -> Environment Options" and click "Add Environment"
4. Enter name "Python 3.3 Source Engine"
5. Enter "Path": path\to\py-source-sdk-2013\mp\game\pysource\python\vspt_server.bat
6. Enter "Window Path": path\to\py-source-sdk-2013\mp\game\pysource\python\vspt_server.bat
7. Enter "Library Path": path\to\py-source-sdk-2013\mp\game\pysource\python\Lib
8. Set Architecture to "x86" and Language Version to "3.3"
9. Go to "View -> Other Windows -> Python Environments". In the new tab press "Refresh DB" on the "Python 3.3 Source Engine" entry

This will update the Intellisense database. It launches the game in text mode to do so. You can now test the environment by clicking
''Interactive Window'' (type something like "import entities", followed by "entities." to see intellisense working).

Follow these steps to start a debugging session using VSPT:

1. Open [Python.sln](mp/game/pysource/python/python.sln)
2. Remove the "Unknown Python 3.3" entry from "Python Environments" in the project
3. Add "Python 3.3 Source Engine" to the project
4. Go to properties of "Python.sln"
5. Go to the Debug tab
6. Add "-sv -noborder -dev -game "path\to\pysource" -vsptdebug" to "Interpreter Arguments"
7. Add "path\to\SteamApps\common\Source SDK Base 2013 Multiplayer\hl2.exe" to "Interpreter Path"
8. Debug -> Start Debugging

Try set a breakpoint in ''examples/commands.py'' to verify debugging works.

## Generating new modules
PySource makes use of gccxml, pygccxml and pyplusplus to generate Boost Python bindings.
You can find instructions in [mp/src/srcpypp](mp/src/srcpypp).

## List of binding modules
- [_animation](mp/src/game/shared/python/modules/_animation.py): Exposed functions from - [animation.h](mp/src/game/shared/animation.h)
- [_entities](mp/src/game/shared/python/modules/_entities.py): Exposes most base entity classes (CBaseEntity, CBaseAnimating, etc)
- [_entitiesmisc](mp/src/game/shared/python/modules/_entitiesmisc.py): Exposes miscellaneous bindings related to entities, like the entity list
- [_gamerules](mp/src/game/shared/python/modules/_gamerules.py): Exposes Gamerules classes. Allows creating and installing custom Gamerules on the fly.
- [_physics](mp/src/game/shared/python/modules/_physics.py): Exposed IPhysicsObject and related.
- [_gameinterface](mp/src/game/shared/python/modules/_gameinterface.py): Exposes game engine interface, user messages, ConCommands and ConVars among others.
- [_ndebugoverlay](mp/src/game/shared/python/modules/_ndebugoverlay.py): Exposes [NDebugOverlay](mp/src/game/shared/debugoverlay_shared.h) functions.
- [_particles](mp/src/game/shared/python/modules/_particles.py): Exposed Particle system related functions, like DispatchParticleEffect.
- [_sound](mp/src/game/shared/python/modules/_sound.py): Exposes sound engine interface and related.
- [srcbuiltins](mp/src/game/shared/python/modules/srcbuiltins.py): Exposes debug Msg functions, used for redirecting output of Python
- [steam](mp/src/game/shared/python/modules/steam.py): Exposes steam api related classes.
- [_te](mp/src/game/shared/python/modules/_te.py): Exposes temporary effects/entities, client side effects and FX_ functions
- [_utils](mp/src/game/shared/python/modules/_utils.py): Exposes utils functions and related (e.g. UTIL_TraceLine)
- [_vmath](mp/src/game/shared/python/modules/_vmath.py): Exposes mathlib
- [vprof](mp/src/game/shared/python/modules/vprof.py): Exposes VProfiling

Note: Most of these modules are complemented by [Python modules](mp/game/pysource/python) (e.g. [entities](mp/game/pysource/python/entities.py))