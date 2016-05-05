
from bots.b_time import BTime
from bots.b_bots import BBots

'''{text, ts, user, team, type, channel}'''

data = {u'text': u'test', u'ts': u'1461950344.000004', u'user': u'U13SD9KSN'
    , u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'D14JN5VNE'}

def update(data, text):
    if 'text' in data:
        data['text'] = text
    return data

#bt = BTime()
#print bt.action("command", "text", None)

bots = BBots()

print "----\nRaw:"
bots.action({u'text': u'testing CMRQ-1500 again', u'ts': u'1462474491.000084', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'C14FTCSKV'})

print "----\nTime:"
print bots.action(update(data, "now"))
print bots.action(update(data, "timestamp"))
print bots.action(update(data, "tell me the time"))
print bots.action(update(data, "what time is it"))
print bots.action(update(data, "time as of now?"))

print "----\nJira:"
print bots.action(update(data, "Ticket SCIOPS-100 needs help"))
print bots.action(update(data, "Ticket CMRQ-1500 is done"))
print bots.action(update(data, "GCMD-100"))
print bots.action(update(data, "CMR-2600 should work"))

print "----\nRPN:"
print bots.action(update(data, "rpn: (1 2 3 + +)"))
print bots.action(update(data, "rpn: (1 2 3 ^ +)"))

print "----\nLang:"
print bots.action(update(data, "What the hell is going on"))
print bots.action(update(data, "Only nice things said here"))
print bots.action(update(data, "frankly dear I don't give a damn!"))
print bots.action(update(data, "frankly dear I don't give a shit!"))

print "----\nEncode:"
print bots.action(update(data, "encode: ({'json':'data'})"))
print bots.action(update(data, "decode: (%7B%27json%27%3A%27data%27%7D)"))

'''
print "----\nCMR:"
bots.action(update(data, "C1214603708-SCIOPS"))
bots.action(update(data, "find: C1214603708-SCIOPS"))
bots.action(update(data, "find: C1214603708-SCIOPS/35"))
bots.action(update(data, "find: msut2"))
bots.action(update(data, "find: msut2_5"))
'''
print "----"
