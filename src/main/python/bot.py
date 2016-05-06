import time
import re
import os.path
import traceback
import calendar
import datetime
from datetime import date

from slackclient import SlackClient

from bots.b_rpn import *
from bots.b_bots import *

'''
This is a bot that listens to a slack project and response with comments


[{u'type': u'user_typing', u'user': u'U13SD9KSN', u'channel': u'D14JN5VNE'}]
[{u'text': u'test', u'ts': u'1461950344.000004', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'D14JN5VNE'}]

[{text, ts, user, team, type, channel}]


{
    u'ok': True
    , u'user':
    {
        u'status': None
        , u'profile':
        {
            u'first_name': u'Chris'
            , u'last_name': u'Gokey'
            , u'image_1024': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_1024.jpg'
            , u'real_name': u'Chris Gokey'
            , u'image_24': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_24.jpg'
            , u'image_original': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_original.jpg'
            , u'real_name_normalized': u'Chris Gokey'
            , u'image_512': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_512.jpg'
            , u'image_32': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_32.jpg'
            , u'image_48': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_48.jpg'
            , u'image_72': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_72.jpg'
            , u'avatar_hash': u'376a1d5ad4b6'
            , u'email': u'cgokey@sesda3.com'
            , u'image_192': u'https://avatars.slack-edge.com/2016-05-02/39518724470_376a1d5ad4b61e722e68_192.jpg'
        }
        , u'tz': u'America/Indiana/Indianapolis'
        , u'name': u'cgokey'
        , u'deleted': False
        , u'is_bot': False
        , u'tz_label': u'Eastern Daylight Time'
        , u'real_name': u'Chris Gokey'
        , u'color': u'4bbe2e'
        , u'team_id': u'T13S7BSJD'
        , u'is_admin': False
        , u'is_ultra_restricted': False
        , u'is_restricted': False
        , u'is_owner': False
        , u'tz_offset': -14400
        , u'id': u'U13RZ7V0U'
        , u'is_primary_owner': False
    }
}

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
    '''
    m = re.search(".*().*", text)
    if m is not None:
        id = m.group(0)
        if id is not None and 0<len(id):
            msg = "%s %s%s" % ("looks like you just mentioned the ticket ", "https://bugs.earthdata.nasa.gov/browse/", id)
            sc.rtm_send_message(channel, msg)
            return True
    '''
    '''
    m = re.search(".*(CMRQ-[\d]{1,4}).*", text)
    if m is not None:
        id = m.group(0)
        if id is not None and 0<len(id):
            msg = "%s %s%s" % ("looks like you just mentioned the ticket ", "https://bugs.earthdata.nasa.gov/browse/", id)
            sc.rtm_send_message(channel, msg)
            return True
    
    m = re.search("(C1[0-9]{8,11}-[-_A-Za-z]{2,10})", text)
    if m is not None:
        id = m.group(0)
        if id is not None and 0<len(id):
            msg = "Were you talking about the collection https://cmr.sit.earthdata.nasa.gov/search/concepts/%s" % id
            sc.rtm_send_message(channel, msg)
            return True
    
    id = match(r"rpn\(([^\)]+)\)", text)
    if id is not None:
        rpn = BRpn()
        if id.startswith("rpn(") and id.endswith(")"):
            id = id[4:-1]
        ans = rpn.math(id)
        msg = "I *love* doing math problems like _'%s'_. The answer is %s." % (id, ans)
        sc.rtm_send_message(channel, msg)
        return True
    
    m = re.search("(current month)", text)
    if m is not None:
        c = calendar.TextCalendar()
        today = date.today()
        cal = c.formatmonth(today.year, today.month)
        if cal is not None:
            msg = cal #.replace("\n", "<br>")
            sc.rtm_send_message(channel, msg)
        return True
    '''
    return False

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
        print sc.api_call('users.info', user='U13RZ7V0U')['user']['real_name']
        if toolbot is not None:
            sc.rtm_send_message(toolbot, "{'text':'I just woke up'}")
        else:
            print (sc)
        
        bots = BBots()
        
        while True:
            data = sc.rtm_read()
            try:
                schedule(sc, gen)
                for datum in data:
                    if "type" in datum:
                        #i = False
                        user = None
                        if "user" in datum:
                            user = sc.api_call("users.info", user=datum["user"])
                        if datum["type"] == "message":
                            if "text" in datum:
                                text = datum["text"]
                                if text is not None:
                                    if "channel" in datum:
                                        channel = datum["channel"]
                                        #list = ["D14JN5VNE", sandbox.id]
                                        #if channel in list:
                                        if not interesting(sc, text, channel):
                                            print "do it the new way"
                                            msg = bots.action(datum)
                                            print "message from %s" % user["user"]["real_name"]
                                            if msg is not None and 0<len(msg):
                                                sc.rtm_send_message(channel, msg)
                        elif datum["type"] == "team_join":
                            print "Welcome %s." % (datum["user"])
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()
                #print sys.exc_info()[0]
            
            if 0<len(data):
                print data
            
            if 5<now.hour and now.hour<20:
                time.sleep(3)
            elif now.hour<5:
                dif = (5*60*60) - (now.hour*60 + hour.minute)*60 + hour.seconds
                time.sleep(dif)
            
    else:
        print "Connection Failed, invalid token?"

if __name__ == "__main__": main()
