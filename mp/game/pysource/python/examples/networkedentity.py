from entities import CBaseEntity, entity
from game.fields import IntegerField

if isserver:
    from entities import FL_EDICT_ALWAYS
else:
    from entities import DATA_UPDATE_CREATED

@entity('netent_example', networked=True)
class NetEntExample(CBaseEntity):
    netvalue = IntegerField(value=0, networked=True, clientchangecallback='OnNetValueChanged')

    def UpdateTransmitState(self):
        ''' This entity is always transmitted to all clients. '''
        return self.SetTransmitState(FL_EDICT_ALWAYS)
        
    def Spawn(self):
        super(NetEntExample, self).Spawn()
        
        print('netent_example spawned on the %s!' % ('Client' if isclient else 'Server'))
        
    def OnDataChanged(self, type):
        super(NetEntExample, self).OnDataChanged(type)
        
        if type == DATA_UPDATE_CREATED:
            print('#%d: netent_example is created on the client' % (self.entindex()))
        
    def OnNetValueChanged(self):
        print('#%d: netvalue changed to %d' % (self.entindex(), self.netvalue))

