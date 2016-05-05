
from bots.b_time import BTime
from bots.b_bots import BBots

'''[{text, ts, user, team, type, channel}]'''

data = [{u'text': u'test', u'ts': u'1461950344.000004', u'user': u'U13SD9KSN'
    , u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'D14JN5VNE'}]

def update(data, text):
    if 'text' in data[0]:
        data[0]['text'] = text
    return data

bt = BTime()
print bt.action("command", "text", None)

bots = BBots()
print "Time:"
bots.action(update(data, "now"))
bots.action(update(data, "timestamp"))
bots.action(update(data, "tell me the time"))
bots.action(update(data, "what time is it"))
bots.action(update(data, "time as of now?"))

print "----\nCMR:"
bots.action(update(data, "C10000-SCIOPS"))

print "----\nJira:"
bots.action(update(data, "Ticket SCIOPS-100 needs help"))
bots.action(update(data, "Ticket CMRQ-1500 is done"))
bots.action(update(data, "GCMD-100"))
bots.action(update(data, "CMR-2600 should work"))

print "----\nRPN:"
bots.action(update(data, "rpn: 1 2 3 + +"))
bots.action(update(data, "rpn: 1 2 3 ^ +"))

print "----\nLang:"
bots.action(update(data, "What the hell is going on"))
bots.action(update(data, "Only nice things said here"))
bots.action(update(data, "frankly dear I don't give a damn!"))
bots.action(update(data, "frankly dear I don't give a shit!"))

print "----"
