
from bots.b_time import BTime
from bots.b_bots import BBots

'''{text, ts, user, team, type, channel}'''

data = {u'text': u'test', u'ts': u'1461950344.000004', u'user': u'U13SD9KSN'
    , u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'D14JN5VNE'}

def update(data, text):
    if 'text' in data:
        data['text'] = text
    return data

def pbot(bots, data, str):
    resp = bots.action(update(data, str))
    if resp is not None and 0<len(resp):
        print resp

#bt = BTime()
#print bt.action("command", "text", None)

bots = BBots()

print "----\nRaw:"
bots.action({u'text': u'testing CMRQ-1500 again', u'ts': u'1462474491.000084', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'C14FTCSKV'})

print "----\nTime:"
pbot(bots, data, "now")
pbot(bots, data, "timestamp")
pbot(bots, data, "tell me the time")
pbot(bots, data, "what time is it")
pbot(bots, data, "time as of now?")

print "----\nJira:"
pbot(bots, data, "Ticket SCIOPS-100 needs help")
pbot(bots, data, "Ticket CMRQ-1500 is done")
pbot(bots, data, "GCMD-100")
pbot(bots, data, "CMR-2600 should work")

print "----\nRPN:"
pbot(bots, data, "rpn:(1 2 3 + +)")
pbot(bots, data, "rpn:(1 2 3 ^ +)")

print "----\nLang:"
pbot(bots, data, "What the hell is going on")
pbot(bots, data, "Only nice things said here")
pbot(bots, data, "frankly dear I don't give a damn!")
pbot(bots, data, "frankly dear I don't give a shit!")

print "----\nEncode:"
pbot(bots, data, "encode:({'json':'data'})")
pbot(bots, data, "decode:(%7B%27json%27%3A%27data%27%7D)")

print "----\nCMR:"
pbot(bots, data, "C1214603708-SCIOPS")
print
pbot(bots, data, "id:C1214603708-SCIOPS")
print
pbot(bots, data, "id:C1214603708-SCIOPS/35")
print
pbot(bots, data, "id:msut2")
print
pbot(bots, data, "id:msut2_5")
print
pbot(bots, data, "ids:zzz415")

print "----"
