from gameinterface import CSingleUserRecipientFilter
    
from _utils import *

# Tracer Flags
TRACER_FLAG_WHIZ = 0x0001
TRACER_FLAG_USEATTACHMENT = 0x0002

TRACER_DONT_USE_ATTACHMENT = -1

# To be used with UTIL_ClientPrintAll
HUD_PRINTNOTIFY = 1
HUD_PRINTCONSOLE = 2
HUD_PRINTTALK = 3
HUD_PRINTCENTER = 4

# UTIL_BloodSpray flags
FX_BLOODSPRAY_DROPS = 0x01
FX_BLOODSPRAY_GORE = 0x02
FX_BLOODSPRAY_CLOUD = 0x04
FX_BLOODSPRAY_ALL = 0xFF

def UTIL_StringToVector(value):   
    """ Try to convert a string to a Vector, if possible. The values must be separated by spaces """
    v = value.split()
    if len(v) != 3:
        raise ValueError('Value is not a Vector')
    return Vector(float(v[0]), float(v[1]), float(v[2]))
    
def UTIL_StringToAngle(value):
    """ Try to convert a string to a QAngle, if possible. The values must be separated by spaces """
    v = value.split()
    if len(v) != 3:
        raise ValueError('Value is not a QAngle')
    return QAngle(float(v[0]), float(v[1]), float(v[2]))
    
def UTIL_StringToColor(value):
    """ Try to convert a string to a Color, if possible. The values must be separated by spaces """
    v = value.split()
    if len(v) == 3:
        return Color(float(v[0]), float(v[1]), float(v[2]))
    elif len(v) == 4:
        return Color(float(v[0]), float(v[1]), float(v[2]), float(v[3]))
    raise ValueError('Value is not a Color')

if isserver:
    def ClientPrint(player, msg_dest, msg_name, param1, param2, param3, param4):
        if not player:
            return

        user = CSingleUserRecipientFilter(player)
        user.MakeReliable()

        UTIL_ClientPrintFilter(user, msg_dest, msg_name, param1, param2, param3, param4)
else:
    def ClientPrint(player, msg_dest, msg_name, param1, param2, param3, param4): pass
    
if isserver:
    def UTIL_GetPlayers():
        ''' Gets all connected players. '''
        players = []
        for i in range(1, gpGlobals.maxClients+1):
            player = UTIL_PlayerByIndex(i)
            if not player or not player.IsConnected():
                continue   
            players.append(player)
        return players
else:
    def UTIL_GetPlayers():
        ''' Gets all players client side. 
            Note that other player entities might not exist on a client, even
            though they exist on the server. 
        '''
        players = []
        for i in range(1, gpGlobals.maxClients+1):
            player = UTIL_PlayerByIndex(i)
            if not player:
                continue   
            players.append(player)
        return players