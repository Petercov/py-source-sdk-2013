from _steam import *

# Add wrappers for a few Matchmaking functions
__fnSteamMatchmaking = steamapicontext.SteamMatchmaking
def __SteamMatchmakingModifier():
    matchmaking = __fnSteamMatchmaking()
    matchmaking.GetLobbyDataByIndex = PyGetLobbyDataByIndex # Wrapper
    return matchmaking
steamapicontext.SteamMatchmaking = __SteamMatchmakingModifier