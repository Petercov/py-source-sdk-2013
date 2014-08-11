from _steam import *

# Add a __hash__ and __str__ implementation to CSteamID class
CSteamID.__hash__ = lambda self: self.GetAccountID()
CSteamID.__str__ = lambda self: str(self.ConvertToUint64())

# Add wrappers for a few Matchmaking functions
__fnSteamMatchmaking = steamapicontext.SteamMatchmaking
def __SteamMatchmakingModifier():
    # Add wrappers
    matchmaking = __fnSteamMatchmaking()
    if matchmaking:
        matchmaking.GetLobbyDataByIndex = PyGetLobbyDataByIndex
        matchmaking.SendLobbyChatMsg = PySendLobbyChatMsg
        matchmaking.GetLobbyChatEntry = PyGetLobbyChatEntry
    return matchmaking
steamapicontext.SteamMatchmaking = __SteamMatchmakingModifier

steamapicontext.SteamMatchmakingServers = SteamMatchmakingServers