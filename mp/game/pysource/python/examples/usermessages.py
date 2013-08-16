from game.usermessages import usermessage, usermessage_shared

@usermessage()
def PyExampleUserMessage(intdata, listdata, dictdata, *args, **kwargs):
    print('%s: PyExampleUserMessage received intdata %s, listdata %s and dictdata %s!' % (
            'Client' if isclient else 'Server', intdata, listdata, dictdata))
            
@usermessage_shared()
def PyExampleUserMessageShared(intdata, listdata, dictdata, *args, **kwargs):
    print('%s: PyExampleUserMessage received intdata %s, listdata %s and dictdata %s!' % (
            'Client' if isclient else 'Server', intdata, listdata, dictdata))