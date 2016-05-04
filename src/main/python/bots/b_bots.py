from b_time import *
from b_cmrlookup import *
from b_rpn import *
from b_bad_lang import *

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
        m = re.search(interest, text)
        if m is not None:
            #print "%s: '%s' matching '%s'" % (action, text, interest)
            if action == "time":
                handler = BTime()
            elif action == "cmr":
                handler = BCmrLookup()
            elif action == "rpn":
                handler = BRpn()
            elif action == "lang":
                handler = BBadLang()
        if handler is not None:
            print handler.action(action, data)
    
    def action(self, data):
        self.actIfInterested(".*(time)(?!\\w+).*", "time", data)   #what time is it
        self.actIfInterested(".*(CMRQ-[0-9]+).*", "jira", data)    #CMRQ-1500
        self.actIfInterested("^rpn:(.*)", "rpn", data)
        self.actIfInterested(".*", "lang", data)
        
        '''
        what time is it
        tell me the time
        
        how many records are in CMR
        CMR count
        
        is CMR up
        is GCMD up
        is * up
        
        
        
        '''
    
        