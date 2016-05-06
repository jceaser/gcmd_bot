from b_bad_language import *
from b_cmr_lookup import *
from b_encode import *
from b_jira import *
from b_rpn import *
from b_time import *

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
        if handler is not None:
            ans = handler.action(action, data, m)
            if ans is not None:
                self.msgs.append(ans)
    
    def action(self, data):
        self.msgs = []
        
        self.actIfInterested(".*(time)(?!\\w+).*", "time", data)   #what time is it
        
        self.actIfInterested(".*(C1[0-9]{9}-\w[-_\w]{0,9}).*", "cmr", data) #C1214603708-SCIOPS
        self.actIfInterested("id:([_a-zA-Z0-9]+)", "cmr", data)     #id:msut2_5
        self.actIfInterested("ids:([_a-zA-Z0-9]+)", "cmr_all", data)     #id:msut2_5
        
        self.actIfInterested(".*(SCIOPS-[0-9]+).*", "jira", data)   #SCIOPS-1500
        self.actIfInterested(".*(CMRQ-[0-9]+).*", "jira", data)     #CMRQ-1500
        self.actIfInterested(".*(GCMD-[0-9]+).*", "jira", data)     #GCMD-1500
        self.actIfInterested(".*(CMR-[0-9]+).*", "jira", data)      #CMR-1500
        
        self.actIfInterested(".*rpn:\((.*?)\).*", "rpn", data)      #rpn:(2 2 +)
        
        self.actIfInterested("encode:\((.*)\)", "encode", data)     #encode:(Hi There)
        self.actIfInterested("decode:\((.*)\)", "decode", data)     #decode:(Hi%20There)
        
        self.actIfInterested(".*", "lang", data)
        
        if self.msgs is not None and 0<len(self.msgs):
            msg = "\n".join(self.msgs)
            return msg
        else:
            return None
        
def main(argv):
    bots = BBots()
    print bots.action("{u'text': u'testing CMRQ-1500 again', u'ts': u'1462474491.000084', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'C14FTCSKV'}")

if __name__ == "__main__": main(sys.argv[1:])
