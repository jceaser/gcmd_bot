from b_bad_language import *
from b_cmr_lookup import *
from b_encode import *
from b_jira import *
from b_rpn import *
from b_time import *
from b_remember import *
from b_room import *
from b_download import *
from b_weather import *

import re

'''
data = [{u'text': u'test', u'ts': u'1461950344.000004', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'D14JN5VNE'}]
'''

class BBots:
    def __init__(self):
        self.msgs = []
    def actIfInterested(self, interest, action, data={}):
        handler = None
        #for d in data:
        if 'text' in data:
            text = data['text']
        else:
            return
        m = re.match(interest, text)
        
        list = re.finditer(interest, text)
        for m in list:
            if m is not None:
                if action == "time":
                    handler = BTime()
                elif action == "cmr":
                    handler = BCmrLookup()
                elif action == "cmr_all":
                    handler = BCmrLookup()
                elif action == "jira":
                    handler = BJira()
                elif action == "rpn":
                    handler = BRpn()
                elif action == "lang":
                    handler = BBadLang()
                elif action == "encode":
                    handler = BEncode()
                elif action == "decode":
                    handler = BDecode()
                elif action == "remember":
                    handler = BRemember()
                elif action == "recall":
                    handler = BRecall()
                
                elif action == "room":
                    handler = BRoom()
                    handler.mode = "room"
                
                elif action == "hangout":
                    handler = BRoom()
                    handler.mode = "hangout"
                
                elif action == "download":
                    handler = BDown()
                elif action == "weather":
                    handler = BWeather()
                elif action == "help":
                    self.manual()
            if handler is not None:
                ans = handler.action(action, data, m)
                if ans is not None:
                    self.msgs.append(ans)
    
    def action(self, data):
        self.msgs = []
        if type(data) is dict:
            pass
        elif type(data) is list:
            for i in data:
                self.msgs.append(self.action, i)
        elif type(data) is str:
            data = {
                u'text': data
                , u'ts': str(datetime.datetime.now())
                , u'user': u'Unspecified'
                , u'team': u'Unspecified'
                , u'type': u'message'
                , u'channel': u'Unspecified'
            }

        
        self.actIfInterested(r"(toolbot(, )?)?what can I do here(\?)+", "help", data)
        self.actIfInterested(r"(toolbot(, )?)?help me!+", "help", data)
        self.actIfInterested(r"(help me toolbot)", "help", data)
        
        self.actIfInterested(".*(what time is it)(?!\\w+).*", "time", data)     #what time is it
        
        self.actIfInterested(r"\b(C1[0-9]{9}-\w[-_\w]{0,9})\b", "cmr", data)    #C1214603708-SCIOPS
        self.actIfInterested(r"\bid:([\./:_a-zA-Z0-9]+)\b", "cmr", data)        #id:msut2_5
        self.actIfInterested(r"\bids:([\./:_a-zA-Z0-9]+)\b", "cmr_all", data)   #id:msut2_5
        
        self.actIfInterested(r"\b(SCIOPS-[0-9]+)\b", "jira", data)   #SCIOPS-1500
        self.actIfInterested(r"\b(CMRQ-[0-9]+)\b", "jira", data)     #CMRQ-1500
        self.actIfInterested(r"\b(GCMD-[0-9]+)\b", "jira", data)     #GCMD-1500
        self.actIfInterested(r"\b(CMR-[0-9]+)\b", "jira", data)      #CMR-1500
        self.actIfInterested(r"\b(MMT-[0-9]+)\b", "jira", data)   #MMT-1500
        
        self.actIfInterested(r"\brpn:\(([^\)\b]*)\)", "rpn", data)      #rpn:(2 2 +)
        #self.actIfInterested(".*rpn:\((.*?)\).*", "rpn", data)      #rpn:(2 2 +)
        
        self.actIfInterested(r"\bencode:\((.*)\)", "encode", data)     #encode:(Hi There)
        self.actIfInterested(r"\bdecode:\((.*)\)", "decode", data)     #decode:(Hi%20There)
        
        self.actIfInterested(r"\bremember:\(([a-zA-z]+)\s(.*)\)", "remember", data)
        self.actIfInterested(r"\brecall:\(([a-zA-Z]+)\)", "recall", data)
        
        self.actIfInterested(r"\\room", "room", data)
        self.actIfInterested(r"\\hangout", "hangout", data)
        
        self.actIfInterested(r"\b(local weather)\b", "weather", data)
        
        self.actIfInterested(r"\bget:\((.*)\)", "download", data)     #get:(http://url.com)
        
        self.actIfInterested(".*", "lang", data)
        
        
        if self.msgs is not None and 0<len(self.msgs):
            msg = "\n- and -\n".join(self.msgs)
            return msg
        else:
            return None
    
    def manual(self):
        format = "%-25s | %25s"
        self.msgs.append(format % ("Input", "Output"))
        self.msgs.append(format % ("----------", "----------"))
        self.msgs.append(format % ("what time is it", "current time and date"))
        self.msgs.append(format % ("local weather", "current weather"))
        #self.msgs.append(format % ("cal", "calendar"))
        
        self.msgs.append(format % ("rpn:(1 2 +)", "3"))
        self.msgs.append(format % ("encode:(Hi+There)", "Hi%20There"))
        self.msgs.append(format % ("decode:(Hi%20There)", "Hi There"))
        
        self.msgs.append(format % ("C1234567890-Provider", "first URL to record"))
        self.msgs.append(format % ("id:some_cmr_id", "first URL to record"))
        self.msgs.append(format % ("ids:some_cmr_id", "all URLs to record"))
        
        self.msgs.append(format % ("SCIOPS-123", "URL to ticket"))
        self.msgs.append(format % ("CMRQ-123", "URL to ticket"))
        self.msgs.append(format % ("GCMD-123", "URL to ticket"))
        self.msgs.append(format % ("CMR-123", "URL to ticket"))
    
def main(argv):
    bots = BBots()
    print bots.action("{u'text': u'testing CMRQ-1500 again', u'ts': u'1462474491.000084', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'C14FTCSKV'}")

if __name__ == "__main__": main(sys.argv[1:])
