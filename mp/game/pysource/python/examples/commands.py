from gameinterface import concommand
from entities import CreateEntityByName, DispatchSpawn, eventqueue, variant_t
from utils import UTIL_GetCommandClient

print('Registering examples package commands. Use "py_example_*" commands to run the examples!')

@concommand('py_example_entity')
def PyExampleEntity(args):
    # Get the player's origin, which we can use for spawning our entities
    player = UTIL_GetCommandClient()
    origin = player.GetAbsOrigin()
    print('Player origin: %s' % (str(origin)))

    # Register our entity factories by importing the module containing them (if not already imported)
    print('Creating entity classes and factories...')
    from . import entity
    
    # Spawn example_ent at our origin
    entexample = CreateEntityByName('ent_example')
    entexample.SetAbsOrigin(origin)
    DispatchSpawn(entexample)
    entexample.Activate()
    
@concommand('py_example_mylogicalentity')
def PyExampleMyLogicalEntity(args):
    # Get the player's origin, which we can use for spawning our entities
    player = UTIL_GetCommandClient()
    origin = player.GetAbsOrigin()
    print('Player origin: %s' % (str(origin)))

    # Register our entity factories by importing the module containing them (if not already imported)
    print('Creating entity classes and factories...')
    from . import entity
    
    # Spawn my_logical_entity at our origin
    # Also setup key values (as you would have done when adding the entity in Hammer)
    print('Spawning my_logical_entity')
    mylogicalent = CreateEntityByName('my_logical_entity')
    mylogicalent.SetAbsOrigin(origin)
    mylogicalent.KeyValue('name', 'MyFirstCounter')
    mylogicalent.KeyValue('threshold', '3')
    DispatchSpawn(mylogicalent)
    mylogicalent.Activate()
    
    # Now use the entity
    print('Firing Tick inputs to our logical entity. Make sure to put "Developer" to "2" so you can see the inputs being received')
    value = variant_t()
    eventqueue.AddEvent(mylogicalent, "Tick", value, 0.5, None, None)
    eventqueue.AddEvent(mylogicalent, "Tick", value, 0.75, None, None)
    eventqueue.AddEvent(mylogicalent, "Tick", value, 1.0, None, None)
    
@concommand('py_example_networkedentity')
def PyExampleNetworkedEntity(args):
    # Get the player's origin, which we can use for spawning our entities
    player = UTIL_GetCommandClient()
    origin = player.GetAbsOrigin()
    print('Player origin: %s' % (str(origin)))
    
    # Register our entity factories by importing the module containing them (if not already imported)
    print('Creating networked entity classes and factories...')
    from . import networkedentity
    
    # Spawn example_ent at our origin
    entexample = CreateEntityByName('netent_example')
    entexample.SetAbsOrigin(origin)
    DispatchSpawn(entexample)
    entexample.Activate()
    