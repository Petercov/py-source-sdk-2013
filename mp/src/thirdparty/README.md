* Compiling Python 3.4 static library
Python 3.4 must be compiled as static library. Instructions per Platform vary a bit.

** Windows
1. Open PCBuild/pcbuild.sln
2. Open properties of PythonCore project
3. In General, change "Configuration Type" to "Static Library"
4. In C/C++ -> Code Generation, change "Runtime Library" to "Multi-threaded (/MT)"
5. Compile the PythonCore project
6. Copy Python34.lib to src\lib\public

** OSX
Open a terminal and go into the python folder.

1. ./configure --enable-shared
2. Open MakeFile and locate "CONFIGURE_CFLAGS"
3. Add "-m32 -static" to CONFIGURE_CFLAGS
3. Add "-m32 -static" to CONFIGURE_CPPFLAGS
3. Add "-m32 -static -read_only_relocs suppress" to CONFIGURE_LDFLAGS
4. make
5. cp libpython3.4m.a ../../lib/public/osx32/libpython3.4m.a

Note python3.4m.dylib will fail to build, however python3.4m.a is still created.
The Makefile is edited because passing these flags to configure will make configure fail due some tests.

** Linux
Open a terminal and go into the python folder.

1. ./configure --enable-shared LDFLAGS="-static -static-libgcc" CPPFLAGS="-static"
2. Open pyconfig.h and comment HAVE_FORKPTY, HAVE_OPENPTY, HAVE_PTY_H, HAVE_CLOCK, HAVE_CLOCK_GETRES, HAVE_CLOCK_GETTIME if needed.
3. make
5. cp python3.4m.a ../../lib/public/linux32/python3.4m.a