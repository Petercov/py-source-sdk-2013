#! /usr/bin/python
''' src_module_builder provides a builder set up for building modules for source sdk code.
'''

from pyplusplus import module_builder
from pygccxml import parser

import platform
import os

# Include directories
incl_paths = [
]

# Defined symbols
basesymbols = [
    '__SSE__',
    '__MMX__',
    
    # Generation
    'PYPP_GENERATION',
]

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
BASE_CFLAGS = '-Wall -Wextra -Wshadow -Wno-invalid-offsetof -fno-strict-aliasing -Wno-unknown-pragmas \
-Wno-unused-parameter -Wno-unused-value -Wno-missing-field-initializers -Wno-sign-compare -Wno-reorder \
-Wno-invalid-offsetof -Wno-float-equal -Werror=return-type -fdiagnostics-show-option -Wformat \
-Wformat-security -fpermissive '
SHLIBEXT = 'so'
SHLIBCFLAGS = '-fPIC '
SHLIBLDFLAGS = '-shared -Wl,-Map,$@_map.txt -Wl '
default_cflags = BASE_CFLAGS


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

        includepaths = list(map(lambda p: p.replace('\\', '/'), includepaths))
        includepaths = list(filter(os.path.normpath, includepaths))
            
        self.definedsymbols = symbols
        self.includes = includepaths

        xml_generator_config = parser.xml_generator_configuration_t( xml_generator_path='castxml'
                                         , working_directory='.'
                                         , include_paths=includepaths
                                         , define_symbols=symbols
                                         , undefine_symbols=usymbols
                                         , start_with_declarations=None
                                         #, ignore_gccxml_output=False
                                         , xml_generator='castxml'
                                         )
        
        module_builder.module_builder_t.__init__(
                    self
                    , files
                    , xml_generator_config=xml_generator_config
                    , cache=None
                    , optimize_queries=True
                    , encoding='ascii'
                    )
