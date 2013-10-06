import os

from . basesource import SourceModuleGenerator
from .. src_module_builder import src_module_builder_t

class ClientModuleGenerator(SourceModuleGenerator):
    module_type = 'client'
    dll_name = 'Client'
    isclient = True
    isserver = False
    
    @property
    def path(self):
        return os.path.join(self.settings.srcpath, self.settings.client_path)
    
    # Create builder
    def CreateBuilder(self, files, parseonlyfiles):
        mb = src_module_builder_t(files, is_client=True)
        mb.parseonlyfiles = parseonlyfiles
        return mb
    

    
