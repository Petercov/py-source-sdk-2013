if isserver:
    from . import commands # Registers console commands for running examples
    from . import entity # Register example entity factories
    
from . import networkedentity # Register example networked entity factory
from . import usermessages # Register example usermessages