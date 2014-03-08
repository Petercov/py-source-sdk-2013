''' Example of creating and installing custom gamerules. '''
from gamerules import CHL2MPRules as BaseClass, InstallGameRules

def InstallCustomGameRules():
    InstallGameRules(CustomGameRules)
    
def ClearCustomGameRules():
    InstallGameRules(None)

class CustomGameRules(BaseClass):
    nextupdate = 0.0

    def Think(self):
        ''' Called per frame. All think logic goes in here. '''
        if gpGlobals.curtime < self.nextupdate:
            return
            
        self.nextupdate = gpGlobals.curtime + 1.0
        
        print('CustomGameRules Think')