'''
Module space used in the "spy" and "cpy" console commands.

Import anything here you want to be available by default in these commands.
'''
import os
import sys
from imp import reload

from game.dispatch import receiver
import entities
from entities import entlist, CBasePlayer
from utils import *

# Set variables
if isserver:
    from game.signals import clientactive
    @receiver(clientactive)
    def __ClientActive(sender, client, **kwargs):
        global player
        if client.entindex() == 1:
            player = client
            
else:
    from game.signals import postlevelinit
    @receiver(postlevelinit)
    def LevelInit(sender, **kwargs): 
        global player
        player = CBasePlayer.GetLocalPlayer()