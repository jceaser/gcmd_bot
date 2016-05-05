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
    
    def actIfInterested(self, interest, action, data):
        handler = None
        for d in data:
            if 'text' in d:
                text = d['text']
                break
        m = re.match(interest, text)
        #if action=="encode":
            #print text
        if m is not None:
            #if action == "encode":
            #    print m.group(1)
            if action == "time":
                handler = BTime()
            elif action == "cmr":
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
            if ans is not None: print ans
    
    def action(self, data):
        self.actIfInterested(".*(time)(?!\\w+).*", "time", data)   #what time is it
        
        self.actIfInterested(".*(C1[0-9]{9}-\w[-_\w]{0,9}).*", "cmr", data)    #CMRQ-1500
        self.actIfInterested("find: ([_a-zA-Z0-9]+)", "cmr", data)    #CMRQ-1500
        
        self.actIfInterested(".*(SCIOPS-[0-9]+).*", "jira", data)    #CMRQ-1500
        self.actIfInterested(".*(CMRQ-[0-9]+).*", "jira", data)    #CMRQ-1500
        self.actIfInterested(".*(GCMD-[0-9]+).*", "jira", data)    #CMRQ-1500
        self.actIfInterested(".*(CMR-[0-9]+).*", "jira", data)    #CMRQ-1500
        
        self.actIfInterested("^rpn:(.*)", "rpn", data)
        
        self.actIfInterested("encode: \((.*)\)", "encode", data)
        self.actIfInterested("decode: \((.*)\)", "decode", data)
        
        self.actIfInterested(".*", "lang", data)
        
        