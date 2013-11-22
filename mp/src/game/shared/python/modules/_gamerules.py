from srcpy.module_generators import SemiSharedModuleGenerator

from pyplusplus.module_builder import call_policies
from pyplusplus import function_transformers as FT
from pygccxml.declarations import matchers

class GameRules(SemiSharedModuleGenerator):
    module_name = '_gamerules'
    split = True
    
    files = [
        'cbase.h',
        'gamerules.h',
        'multiplay_gamerules.h',
        'singleplay_gamerules.h',
        'teamplay_gamerules.h',
        'srcpy_gamerules.h',
        '#hl2mp/hl2mp_player.h',
        'hl2mp/hl2mp_gamerules.h',
        'ammodef.h',
        '#items.h',
        '$takedamageinfo.h',
    ]
    
    gamerules = [
        ('CGameRules', 'C_GameRules'),
        ('CMultiplayRules', 'C_MultiplayRules'),
        ('CSingleplayRules', 'C_SingleplayRules'),
        ('CTeamplayRules', 'C_TeamplayRules'),
        ('CHL2MPRules', 'C_HL2MPRules'),
    ]
        
    def Parse(self, mb):
        # Exclude everything by default
        mb.decls().exclude()
        
        for gamerulename, clientgamerulename in self.gamerules:
            cls_name = gamerulename if self.isserver else clientgamerulename
            cls = mb.class_(cls_name)
            cls.include()
        
            # Used internally
            cls.mem_funs('GetPySelf', allow_empty=True).exclude()
            cls.add_wrapper_code(
                'virtual PyObject *GetPySelf() const { return boost::python::detail::wrapper_base_::get_owner(*this); }'
            )
            
            # Always use server class name
            cls.rename(gamerulename)
            
        mb.mem_funs('ShouldCollide').virtuality = 'not virtual'
        mb.mem_funs('GetAmmoDamage').virtuality = 'not virtual' # Just modify the ammo table when needed...
        
        # Gamerules class
        if self.isserver:
            # Call policies
            mb.mem_funs('GetPlayerSpawnSpot').call_policies = call_policies.return_value_policy(call_policies.return_by_value)
            
            mb.mem_funs('GetDeathScorer').call_policies = call_policies.return_value_policy(call_policies.return_by_value)
            mb.mem_funs('VoiceCommand').call_policies = call_policies.return_value_policy(call_policies.return_by_value)
            
            mb.mem_fun('TacticalMissionManagerFactory').exclude()

            # Excludes
            mb.mem_funs('VoiceCommand').exclude()
        else:
            mb.mem_funs('RestartGame').exclude()
            mb.mem_funs('CheckAllPlayersReady').exclude()
            mb.mem_funs('CheckRestartGame').exclude()
            mb.mem_funs('CleanUpMap').exclude()

        mb.mem_funs('GetHL2MPViewVectors').exclude()
            
        # Temp excludes
        mb.mem_funs('GetEncryptionKey').exclude()
        mb.mem_funs('GetViewVectors').exclude()

        # Call policies
        mb.mem_funs('GetNextBestWeapon').call_policies = call_policies.return_value_policy(call_policies.return_by_value)  
        
        # Hide instance
        mb.free_function('PyGameRules').include()
        mb.free_function('PyGameRules').rename('GameRules')
        
        # Installing the gamerules
        mb.free_function('PyInstallGameRules').include()
        mb.free_function('PyInstallGameRules').rename('InstallGameRules')
        
        # CAmmoDef
        mb.class_('CAmmoDef').include()
        mb.class_('CAmmoDef').mem_fun('GetAmmoOfIndex').exclude()
        mb.class_('CAmmoDef').vars('m_AmmoType').exclude()
        
        mb.free_function('GetAmmoDef').include()
        mb.free_function('GetAmmoDef').call_policies = call_policies.return_value_policy(call_policies.reference_existing_object)
        
        # Remove any protected function 
        mb.calldefs( matchers.access_type_matcher_t('protected') ).exclude()  
    