'''
Module space used in the "spy" and "cpy" console commands.

Import anything here you want to be available by default in these commands.
'''
import os
import sys
from vmath import *
from gameinterface import engine, ConVarRef
from imp import reload

from core.dispatch import receiver
import entities
from entities import entlist, CBasePlayer
from utils import *
if isclient:
    from entities import ClientEntityList
from gamerules import GameRules, gamerules
from steam import steamapicontext

# Set variables
if isserver:
    from core.signals import clientactive
    @receiver(clientactive)
    def __ClientActive(sender, client, **kwargs):
        global player
        if client.entindex() == 1:
            player = client
            
else:
    from core.signals import postlevelinit
    @receiver(postlevelinit)
    def LevelInit(sender, **kwargs): 
        global player
        player = CBasePlayer.GetLocalPlayer()