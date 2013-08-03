from entities import CBaseEntity, CLogicalEntity, entity
from game.fields import IntegerField, OutputField, input

# Stripped down example of creating a new entity
# The entity class must be derived from BaseEntity
# The entity factory is created by the decorator "entity". The first argument is the entity name.
@entity('ent_example')
class EntExample(CBaseEntity):
    def Spawn(self):
        super(EntExample, self).Spawn()
        
        print('ent_example spawned!')

# Python Example of https://developer.valvesoftware.com/wiki/Authoring_a_Logical_Entity
@entity('my_logical_entity')
class CMyLogicalEntity(CLogicalEntity):
    #: Count at which to fire our output
    counter = IntegerField(value=0)
    #: Internal counter
    threshold = IntegerField(value=0, keyname='threshold')
    #: Output event when the counter reaches the threshold
    onthreshold = OutputField(keyname='OnThreshold')
    
    @input('Tick')
    def InputTick(self, inputdata):
        ''' Handle a tick input from another entity '''
        # Increment our counter
        self.counter += 1
        
        # See if we've met or crossed our threshold value
        if self.counter >= self.threshold:
            # Fire an output event
            self.onthreshold.FireOutput(inputdata.activator, self)
            
            # Reset our counter
            self.counter = 0
        
        