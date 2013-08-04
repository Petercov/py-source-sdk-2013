from vmath import Vector, QAngle, vec3_origin, VectorAngles, RandomVector
from entities import CBaseEntity, CLogicalEntity, CBaseAnimating, entity, SOLID_BBOX, MOVETYPE_FLY, MOVETYPE_NONE
from utils import UTIL_SetSize
from game.fields import IntegerField, BooleanField, FloatField, OutputField, input

import random

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
        
# Python example of https://developer.valvesoftware.com/wiki/Authoring_a_Model_Entity
@entity('my_model_entity')
class CMyModelEntity(CBaseAnimating):
    # Name of our entity's model
    ENTITY_MODEL = "models/gibs/airboat_broken_engine.mdl"
    
    active = BooleanField(value=False)
    nextchangetime = FloatField(value=0.0)

    def Spawn(self):
        self.Precache()
     
        self.SetModel(self.ENTITY_MODEL)
        self.SetSolid(SOLID_BBOX)
        UTIL_SetSize(self, -Vector(20,20,20), Vector(20,20,20))
        
    def Precache(self):
        self.PrecacheModel(self.ENTITY_MODEL)
     
        super(CMyModelEntity, self).Precache()
    
    def MoveThink(self):
        # See if we should change direction again
        if self.nextchangetime < gpGlobals.curtime:
            # Randomly take a new direction and speed
            newvelocity = RandomVector(-64.0, 64.0)
            self.SetAbsVelocity(newvelocity)
     
            # Randomly change it again within one to three seconds
            self.nextchangetime = gpGlobals.curtime + random.uniform(1.0, 3.0)
     
        # Snap our facing to where we're heading
        vecfacing = self.GetAbsVelocity()
        angfacing = QAngle()
        VectorAngles(vecfacing, angfacing)
        self.SetAbsAngles(angfacing)
     
        # Think at 20Hz
        self.SetNextThink(gpGlobals.curtime + 0.05)

    @input('Toggle')
    def InputToggle(self, inputdata):
        # Toggle our active state
        if not self.active:
            # Start thinking
            self.SetThink(self.MoveThink)
     
            self.SetNextThink(gpGlobals.curtime + 0.05)
     
            # Start moving
            self.SetMoveType(MOVETYPE_FLY)
     
            # Force MoveThink() to choose a new speed and direction immediately
            self.nextchangetime = gpGlobals.curtime
     
            # Update self.active to reflect our new state
            self.active = True
        else:
            # Stop thinking
            self.SetThink(None)
     
            # Stop moving
            self.SetAbsVelocity(vec3_origin)
            self.SetMoveType(MOVETYPE_NONE)
     
            self.active = False
    