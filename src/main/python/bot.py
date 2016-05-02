import time
from slackclient import SlackClient
import re
import os.path
import calendar
from datetime import date
import datetime
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

def interesting(sc, text, channel):
    m = re.search("(CMRQ-[\d]+)", text)
    if m is not None:
        id = m.group(0)
        msg = "%s %s%s" % ("looks like you just mentioned the ticket ", "https://bugs.earthdata.nasa.gov/browse/", id)
        sc.rtm_send_message(channel, msg)
        return
    
    m = re.search("(C1[0-9]+-[a-z]+)", text)
    if m is not None:
        id = m.group(0)
        msg = "Were you talking about the collection https://cmr.sit.earthdata.nasa.gov/search/concepts/%s" % id
        sc.rtm_send_message(channel, msg)
        return
    
    m = re.search("(current month)", text)
    if m is not None:
        c = calendar.TextCalendar()
        today = date.today()
        cal = c.formatmonth(today.year, today.month)
        if cal is not None:
            msg = cal #.replace("\n", "<br>")
            sc.rtm_send_message(channel, msg)
        return

def schedule(sc, gen):
    today = datetime.date.today()
    now = datetime.datetime.now()
    
    if today.weekday()==2:
        if now.hour == 11 and now.minute == 0 and now.second == 0:
            sc.rtm_send_message(gen.id, "Time for lunch soon")

    if now.hour == 5 and now.minute == 1 and now.second == 0:
        sc.rtm_send_message(gen.id, "Go home, I need these computers to myself.")
    
    if now.hour == 15 and now.minute == 14 and now.second == 16:
        sc.rtm_send_message(gen.id, "Time for pi")
    
def main():
    sc = SlackClient(stringFromFiles())
    if sc.rtm_connect():
        #print sc.server.channels.find("D14JN5VNE")
        sandbox = sc.server.channels.find("sandbox")
        gen = sc.server.channels.find("general")
        
        while True:
            data = sc.rtm_read()
            schedule(sc, gen)
            for datum in data:
                if "type" in datum and datum["type"] == "message":
                    if "text" in datum:
                        text = datum["text"]
                        if text is not None:
                            if "channel" in datum:
                                channel = datum["channel"]
                                #list = ["D14JN5VNE", sandbox.id]
                                #if channel in list:
                                interesting(sc, text, channel)
            #print data
            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"

if __name__ == "__main__": main()
