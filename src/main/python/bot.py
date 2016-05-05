import time
import re
import os.path
import traceback
import calendar
import datetime
from datetime import date

from slackclient import SlackClient

from bots.b_rpn import *

'''
This is a bot that listens to a slack project and response with comments


[{u'type': u'user_typing', u'user': u'U13SD9KSN', u'channel': u'D14JN5VNE'}]
[{u'text': u'test', u'ts': u'1461950344.000004', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'D14JN5VNE'}]

[{text, ts, user, team, type, channel}]

'''

def stringFromFiles():
    text = stringFromFile(".token.txt")
    if (text is None):
        text = stringFromFile("~/.token.txt")
    if (text is None):
        text = stringFromFile("~/.slack_token.txt")
    if (text is None):
        text = stringFromFile("/usr/local/etc/slack_token.txt")
    if text is not None:
        text = text.strip()
    return text

def stringFromFile(file):
    string = None
    if os.path.isfile(file):
        f = open(file,"r")
        string = f.read()
    return string

def match(regex, text):
    ret = None
    m = re.search(regex, text)
    if m is not None:
        id = m.group(0)
        if id is not None and 0<len(id):
            ret = id
    return ret

def interesting(sc, text, channel):
    m = re.search(".*(CMRQ-[\d]{1,4}).*", text)
    if m is not None:
        id = m.group(0)
        if id is not None and 0<len(id):
            msg = "%s %s%s" % ("looks like you just mentioned the ticket ", "https://bugs.earthdata.nasa.gov/browse/", id)
            sc.rtm_send_message(channel, msg)
            return
    
    m = re.search("(C1[0-9]{8,11}-[-_A-Za-z]{2,10})", text)
    if m is not None:
        id = m.group(0)
        if id is not None and 0<len(id):
            msg = "Were you talking about the collection https://cmr.sit.earthdata.nasa.gov/search/concepts/%s" % id
            sc.rtm_send_message(channel, msg)
            return
    
    id = match(r"rpn\(([^\)]+)\)", text)
    if id is not None:
        rpn = BRpn()
        if id.startswith("rpn(") and id.endswith(")"):
            id = id[4:-1]
        ans = rpn.math(id)
        msg = "I *love* doing math problems like _'%s'_. The answer is %s." % (id, ans)
        sc.rtm_send_message(channel, msg)
        return
    
    '''
    m = re.search("(current month)", text)
    if m is not None:
        c = calendar.TextCalendar()
        today = date.today()
        cal = c.formatmonth(today.year, today.month)
        if cal is not None:
            msg = cal #.replace("\n", "<br>")
            sc.rtm_send_message(channel, msg)
        return
    '''

def schedule(sc, gen):
    today = datetime.date.today()
    now = datetime.datetime.now()
    
    if today.weekday()==2:
        if now.hour == 11 and now.minute == 0 and now.second == 0:
            sc.rtm_send_message(gen.id, "Time for lunch soon.")

    if now.hour == 18 and now.minute == 1 and now.second == 0:
        sc.rtm_send_message(gen.id, "Go home, I need these computers to myself.")
    
    if now.hour == 15 and now.minute == 14 and now.second == 16:
        sc.rtm_send_message(gen.id, "Time for pi.")
    
def main():
    sc = SlackClient(stringFromFiles())
    if sc.rtm_connect():
        #print sc.server.channels.find("D14JN5VNE")
        sandbox = sc.server.channels.find("sandbox")
        gen = sc.server.channels.find("general")
        
        toolbot = sc.server.channels.find("Tooly McToolbot")
        if toolbot is not None:
            sc.rtm_send_message(toolbot, "{'text':'I just woke up'}")
        else:
            print (sc)
        
        while True:
            data = sc.rtm_read()
            try:
                schedule(sc, gen)
                for datum in data:
                    if "type" in datum:
                        if datum["type"] == "message":
                            if "text" in datum:
                                text = datum["text"]
                                if text is not None:
                                    if "channel" in datum:
                                        channel = datum["channel"]
                                        #list = ["D14JN5VNE", sandbox.id]
                                        #if channel in list:
                                        interesting(sc, text, channel)
                        elif datum["type"] == "team_join":
                            print "Welcome back %s." % (datum["user"])
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()
                #print sys.exc_info()[0]
            
            if 0<len(data):
                print data
            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"

if __name__ == "__main__": main()
