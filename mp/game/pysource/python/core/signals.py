"""
Game signals.
"""
from .dispatch import Signal
from collections import defaultdict

def FireSignalRobust(s, **kwargs):
    """ Fires the signal directly with the provided arguments.
    
        Prints any exception as a warning.
    """
    responses = s.send_robust(None, **kwargs)
    for r in responses:
        if isinstance(r[1], Exception):
            PrintWarning('Error in receiver %s (module: %s): %s\n' % (r[0], r[0].__module__, r[1]))
            
def _CheckReponses(responses):
    for r in responses:
        if isinstance(r[1], Exception):
            PrintWarning('Error in receiver %s (module: %s): \n%s' %
                (r[0], r[0].__module__, r[2]))
            
def _CallSignal(method, kwargs):
    _CheckReponses(method(**kwargs))

LevelInitSignal = Signal
            
# The level signals are send from src_python.cpp.
# Send at level initialization before entities are spawned
prelevelinit = LevelInitSignal()
map_prelevelinit = defaultdict(lambda : LevelInitSignal())

# Send at level initialization after entities are spawned
postlevelinit = LevelInitSignal()
map_postlevelinit = defaultdict(lambda : LevelInitSignal())

# Send at level shutdown before entities are removed
prelevelshutdown = Signal()
map_prelevelshutdown = defaultdict(lambda : Signal())

# Send at level shutdown after entities are removed
postlevelshutdown = Signal()
map_postlevelshutdown = defaultdict(lambda : Signal())

if isserver:
    # Send when a new client connected
    clientactive = Signal(providing_args=['client'])
    map_clientactive = defaultdict(lambda : Signal(providing_args=['client']))
    
# Called before initializing new gamerules
preinitgamerules = Signal(providing_args=['gamerules'])
# Called after initializing new gamerules
postinitgamerules = Signal(providing_args=['gamerules'])

'''
# Examples of several signals:
from core.dispatch import receiver

@receiver(prelevelinit)
def on_prelevelinit(sender, **kwargs):
    print "Pre Level init callback!"
    
@receiver(map_prelevelinit['wmp_forest'])
def on_prelevelinit(sender, **kwargs):
    print "Pre Level init callback wmp_forest!"
    
@receiver(postlevelinit)
def on_postlevelinit(sender, bla, **kwargs):
    print "Post Level init callback!"
    
@receiver(prelevelshutdown)
def on_prelevelshutdown(sender, **kwargs):
    print "Pre Level shutdown callback!"
    
@receiver(postlevelshutdown)
def on_postlevelshutdown(sender, **kwargs):
    print "Post Level shutdown callback!"
    
if isserver:
    @receiver(clientactive)
    def on_clientactive(sender, client, **kwargs):
        print "client active %s" % (client)
    
'''