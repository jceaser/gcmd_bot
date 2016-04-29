import time
from slackclient import SlackClient
import re

token = "xoxb-38623745957-bkZ6QasIVeZbskwUJuvoOGwV"

sc = SlackClient(token)

print (sc)

'''
[{u'type': u'user_typing', u'user': u'U13SD9KSN', u'channel': u'D14JN5VNE'}]
[{u'text': u'test', u'ts': u'1461950344.000004', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'D14JN5VNE'}]

[{text, ts, user, team, type, channel}]

'''

def interesting(sc, text):
    m = re.search("(CMRQ-[\d]+)", text)
    if m is not None:
        id = m.group(0)
        msg = "%s %s%s" % ("looks like you just mentioned the ticket ", "https://bugs.earthdata.nasa.gov/browse/", id)
        sc.rtm_send_message("D14JN5VNE", msg)

if sc.rtm_connect():
    while True:
        data = sc.rtm_read()
        for datum in data:
            if "type" in datum and datum["type"] == "message":
                if "text" in datum:
                    text = datum["text"]
                    if "channel" in datum and datum["channel"] == "D14JN5VNE":
                        interesting(sc, text)
        print data
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"

