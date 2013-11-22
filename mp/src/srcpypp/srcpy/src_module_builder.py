#! /usr/bin/python
''' src_module_builder provides a builder set up for building modules for source sdk code.
'''

from pyplusplus import module_builder
from pygccxml import parser

import platform
import os

# Include directories
incl_paths = [
    # GCCXML Support files
    '../../srcpypp/Support/GCC/4.6',
    
    # System Headers/Default include paths by GCC (basically a copy of the usr folder of Ubuntu 10.04 32 bit)
    '../../srcpypp/Support/GCC/4.6/usr/lib/gcc/i686-linux-gnu/4.6/include',
    '../../srcpypp/Support/GCC/4.6/usr/lib/gcc/i686-linux-gnu/4.6/include-fixed',
    '../../srcpypp/Support/GCC/4.6/usr/include/c++/4.6',
    '../../srcpypp/Support/GCC/4.6/usr/include/c++/4.6/i686-linux-gnu',
    '../../srcpypp/Support/GCC/4.6/usr/include/i386-linux-gnu',
    '../../srcpypp/Support/GCC/4.6/usr/include',
    
    # Game
    #'../../common',
    #'../../public',
    #'../../public/tier0',
    #'../../public/tier1',
    #'../../game/shared',
    #'../../game/shared/python',
    
    # Python/Boost folders
    #'../../thirdparty/python/Include',
    #'../../thirdparty/python',
    
    # Boost stub headers
    #'../thirdparty/boost',
    #'../srcpypp/boost_stubs',
]
'''
incl_paths_client = [
    '../../game/client', 
    '../../game/client/python',
]
incl_paths_server = [
    '../../game/server', 
    '../../game/server/python',
]
'''
# Defined symbols
basesymbols = [
    '__SSE__',
    '__MMX__',
    
    # Generation
    'PYPP_GENERATION',
]
'''
dsymbols = [
    'NDEBUG',
    'POSIX',
    'GNUC',
    'LINUX',
    '_LINUX',
    'RAD_TELEMETRY_DISABLED',
    'BINK_VIDEO',
    'GL_GLEXT_PROTOTYPES',
    'DX_TO_GL_ABSTRACTION',
    'USE_SDL',
    'VECTOR',
    'VERSION_SAFE_STEAM_API_INTERFACES',
    'PROTECTED_THINGS_ENABLE',
    'sprintf=use_Q_snprintf_instead_of_sprintf',
    'strncpy=use_Q_strncpy_instead',
    '_snprintf=use_Q_snprintf_instead',
    'SWDS',
    'HL2MP',
    'HL2_DLL',
    '_EXTERNAL_DLL_EXT=.so',
    'VPCGAMECAPS=HL2MP',
    'PROJECTDIR=/home/VALVE/joe/p4clients/linuxsdk/hl2/src/game/server',
    '_DLL_EXT=.so',
    'VPCGAME=hl2mp',
    '_LINUX=1',
    '_POSIX=1',
    'LINUX=1',
    'POSIX=1',
    
    'GLOWS_ENABLE',
    
    'BOOST_AUTO_LINK_NOMANGLE',
    'BOOST_PYTHON_STATIC_LIB',
    'BOOST_PYTHON_NO_PY_SIGNATURES',
    'BOOST_SERIALIZATION_NO_LIB',
    'BOOST_PYTHON_MAX_ARITY=20',
    'Py_NO_ENABLE_SHARED',
    'Py_BUILD_CORE',
    'ENABLE_PYTHON',

    '__SSE__',
    '__MMX__',
    
    # Generation
    'PYPP_GENERATION',
]

dsymbols_client = [ 
    'CLIENT_DLL' 
]
dsymbols_server = [
    'GAME_DLL' 
]'''

# Undefined symbols
usymbols = [
    'sprintf=use_Q_snprintf_instead_of_sprintf',
    'strncpy=use_Q_strncpy_instead',
    'fopen=dont_use_fopen',
    'PROTECTED_THINGS_ENABLE',
]

# cflags
ARCH = 'x86_64'
ARCH_CFLAGS = '-mtune=i686 -march=pentium3 -mmmx -m32 '
BASE_CFLAGS = '-Wall -Wextra -Wshadow -Wno-invalid-offsetof -fno-strict-aliasing -Wno-unknown-pragmas -Wno-unused-parameter -Wno-unused-value -Wno-missing-field-initializers -Wno-sign-compare -Wno-reorder -Wno-invalid-offsetof -Wno-float-equal -Werror=return-type -fdiagnostics-show-option -Wformat -Wformat-security -fpermissive '
SHLIBEXT = 'so'
SHLIBCFLAGS = '-fPIC '
SHLIBLDFLAGS = '-shared -Wl,-Map,$@_map.txt -Wl '
default_cflags = ARCH_CFLAGS+BASE_CFLAGS+SHLIBCFLAGS#+'-fpermissive '

if platform.system() == 'Windows':
    gccbinpath = '../../srcpypp/gccxml_bin/win32'
elif platform.system() == 'Linux':
    gccbinpath = '../../srcpypp/gccxml_bin/linux'
else:
    gccbinpath = '../../srcpypp/gccxml_bin/mac'

# NOTE: module_builder_t == builder_t
class src_module_builder_t(module_builder.module_builder_t):
    """
    This is basically a wrapper module with the arguments already setted up for source.
    """

    def __init__(   self
                    , files
                    , includes
                    , symbols
                    , is_client = False
                ): 
        symbols = list(basesymbols + symbols)
        
        includepaths = incl_paths + includes
        includepaths.append('../../srcpypp/boost_stubs')

        includepaths = list(map(lambda p: p.replace('\\', '/'), includepaths))
        includepaths = list(filter(os.path.normpath, includepaths))
            
        self.definedsymbols = symbols
        self.includes = includepaths
        
        module_builder.module_builder_t.__init__(
                    self
                    , files
                    , gccxml_path=gccbinpath
                    , working_directory='.'
                    , include_paths=includepaths
                    , define_symbols=symbols
                    , undefine_symbols=usymbols
                    , start_with_declarations=None
                    , compilation_mode=parser.COMPILATION_MODE.ALL_AT_ONCE
                    , cache=None
                    , optimize_queries=True
                    , ignore_gccxml_output=False
                    , indexing_suite_version=1
                    , cflags=default_cflags+' --gccxml-config "../../srcpypp/gccxml_config" --gccxml-gcc-options "../../srcpypp/gccxml_gcc_options"'
                    , encoding='ascii'
                    #, compiler=None
                    #, gccxml_config=None
                    )
