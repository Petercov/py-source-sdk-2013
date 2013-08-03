from entities import CBaseEntity, entity
from game.fields import IntegerField

if isserver:
    from entities import FL_EDICT_ALWAYS

@entity('netent_example', networked=True)
class NetEntExample(CBaseEntity):
    netvalue = IntegerField(value=0, networked=True, clientchangecallback='OnNetValueChanged')

    def UpdateTransmitState(self):
        ''' This entity is always transmitted to all clients. '''
        return self.SetTransmitState(FL_EDICT_ALWAYS)
        
    def Spawn(self):
        super(NetEntExample, self).Spawn()
        
        print('netent_example spawned on the %s!' % ('Client' if isclient else 'Server'))
        
    def OnNetValueChanged(self):
        print('netvalue changed to %d' % (self.netvalue))

