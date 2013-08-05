from srcpy.module_generators import SharedModuleGenerator
from pyplusplus import code_creators
from pyplusplus import function_transformers as FT
from pyplusplus.module_builder import call_policies

class SrcBuiltins(SharedModuleGenerator):
    module_name = 'srcbuiltins'
    
    files = [
        'srcpy_srcbuiltins.h',
        'Color.h',
        'globalvars_base.h',
        'edict.h',
    ]
    
    def Parse(self, mb):
        # Exclude everything by default
        mb.decls().exclude()      
        
        # Include message functions and rename them
        mb.free_function('SrcPyMsg').include()
        mb.free_function('SrcPyWarning').include()
        mb.free_function('SrcPyDevMsg').include()
        
        mb.free_function('SrcPyMsg').rename('Msg')
        mb.free_function('SrcPyWarning').rename('PrintWarning')
        mb.free_function('SrcPyDevMsg').rename('DevMsg')

        # Include classes for redirecting output (replace stdout and stderr)
        mb.class_('SrcPyStdOut').include()
        mb.class_('SrcPyStdErr').include()
        
        # Color class
        cls = mb.class_('Color')
        cls.include()
        cls.mem_funs('GetColor').add_transformation( FT.output('_r'), FT.output('_g'), FT.output('_b'), FT.output('_a') )
        cls.mem_opers('=').exclude() # Breaks debug mode and don't really need it
        
        # Global Vars Class
        mb.class_('CGlobalVarsBase').include()
        mb.class_('CGlobalVars').include()
        mb.vars('pSaveData').exclude()
        
        # Add converters
        mb.add_registration_code( "bp::to_python_converter<\n\tstring_t,\n\tstring_t_to_python_str>();")
        mb.add_registration_code( "python_str_to_string_t();" )
        mb.add_registration_code( "wchar_t_to_python_str();" )
        mb.add_registration_code( "ptr_wchar_t_to_python_str();" )
        mb.add_registration_code( "python_str_to_wchar_t();" )
        
    def AddAdditionalCode(self, mb):
        header = code_creators.include_t( 'srcpy_srcbuiltins_converters.h' )
        mb.code_creator.adopt_include(header)
        super(SrcBuiltins, self).AddAdditionalCode(mb)