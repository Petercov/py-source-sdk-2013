from entities import CBaseEntity, entity
from core.fields import IntegerField, DictField

if isserver:
    from entities import FL_EDICT_ALWAYS
else:
    from entities import DATA_UPDATE_CREATED

@entity('netent_example', networked=True)
class NetEntExample(CBaseEntity):
    netvalue = IntegerField(value=0, networked=True, clientchangecallback='OnNetValueChanged')
    netdict = DictField(networked=True, clientchangecallback='OnNetDictChanged')

    def UpdateTransmitState(self):
        ''' This entity is always transmitted to all clients. '''
        return self.SetTransmitState(FL_EDICT_ALWAYS)
        
    def Spawn(self):
        super().Spawn()
        
        print('netent_example spawned on the %s!' % ('Client' if isclient else 'Server'))
        
    def OnDataChanged(self, type):
        super().OnDataChanged(type)
        
        if type == DATA_UPDATE_CREATED:
            print('#%d: netent_example is created on the client' % (self.entindex()))
        
    def OnNetValueChanged(self):
        print('#%d: netvalue changed to %d' % (self.entindex(), self.netvalue))

    def OnNetDictChanged(self):
        print('#%d: netdict changed to %s' % (self.entindex(), self.netdict))