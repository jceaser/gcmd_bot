#!/usr/python

import json
import urllib, urllib2
import sys, os

rtmStart = "https://slack.com/api/rtm.start?token=%s&scope=client&simple_latest=true&no_unreads=true"
chatPost = "https://slack.com/api/chat.postMessage?token=%s&channel=%s&text=%s"

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

def main(argv):
    #print "%s %s" % (os.getcwd(), argv[0])
    if len(argv)<1 or argv[0] == "--test":
        return
        
    channel="ttest"
    if 0<len(argv):
        channel = argv[0]
    
    '''
    Send standard in to slack.com
    '''
    token = stringFromFiles()
    req = urllib2.Request(rtmStart % token)
    resp = urllib2.urlopen(req)
    jdat = resp.read()

    data = json.loads(jdat)

    if data['ok']:
        text = ""
        for line in sys.stdin:
            if len(text)<1:
                text = line.strip()
            else:
                text = "%s\\n%s" % (text, line.strip())
        
        for c in data["channels"]:
            #if c['name'] == "sandbox":
            if c['name'] == channel:
                jtemp = '{"id":"1","type":"message","channel":"%s","text": "%s"}'
                jdata2 = jtemp % (c['id'], text.strip())
                
                #post_data = urllib.quote_plus(json.dumps(json.loads(jdata2)))
                post_data = urllib.quote_plus(text.strip())
                cpost_url = chatPost % (token, c['id'], post_data)
                
                print cpost_url
                req2 = urllib2.Request(cpost_url)
                resp2 = urllib2.urlopen(req2)
    else:
        print "Login issue"
    
if __name__ == "__main__": main(sys.argv[1:])
