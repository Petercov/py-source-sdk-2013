from game.usermessages import usermessage, usermessage_shared

# The decorator usermessage turns a method into a usermessage method
# Calling this on the server will result in the method being called on client(s)
# An optional filter keyword argument can be used to control on which clients the method is called
# By default, a CReliableBroadcastRecipientFilter is used
# Internally this uses gameinterface.SendUserMessage, which wraps around UserMessageBegin/MessageEnd
# The arguments types you can send are limited to int, float, str, bool, none, set, dict, list, Vector, QAngle and entity handles.
@usermessage()
def PyExampleUserMessage(intdata, listdata, dictdata, *args, **kwargs):
    print('%s: PyExampleUserMessage received intdata %s, listdata %s and dictdata %s!' % (
            'Client' if isclient else 'Server', intdata, listdata, dictdata))
            
# usermessage_shared is the same as above, but also calls the method on the server
@usermessage_shared()
def PyExampleUserMessageShared(intdata, listdata, dictdata, *args, **kwargs):
    print('%s: PyExampleUserMessage received intdata %s, listdata %s and dictdata %s!' % (
            'Client' if isclient else 'Server', intdata, listdata, dictdata))