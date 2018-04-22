from srcpy.module_generators import ServerModuleGenerator
from pyplusplus import messages
from pygccxml.declarations import matchers

class NavigationMesh(ServerModuleGenerator):
    module_name = '_navmesh'
    
    files = [
        'cbase.h',
        '#nav.h',
        '#nav_area.h',
        '#nav_colors.h',
        '#nav_ladder.h',
        '#nav_mesh.h',
        '#nav_node.h',
        '#nav_pathfind.h'
    ]
    
    def Parse(self, mb): 
        # Exclude everything by default
        mb.decls().exclude()

        mb.classes(lambda decl: 'Nav' in decl.name).include()
        
        # Remove any protected function 
        mb.calldefs( matchers.access_type_matcher_t('protected') ).exclude()

        mb.enumerations().include()

        mb.free_function('NavAreaBuildPath').include()

        # Include the singleton
        var = mb.variable('TheNavMesh')
        var.include()
        var.set_is_read_only(true)

