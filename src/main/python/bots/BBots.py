from BTime import *
from bcmrlookup import *

import re

class BBots:
    
    def actIfInterested(self, interest, cmd, text):
        handler = None
        #print "'%s' matching '%s'" % (text, interest)
        m = re.search(interest, text)
        if m is not None:
            print "%s: '%s' matching '%s'" % (cmd, text, interest)
            if cmd == "time":
                handler = BTime()
            elif cmd == "cmr":
                print "here"
                handler = BCmrLookup()
        if handler is not None:
            print handler.action(cmd, text)
        #else:
        #    print "no handler found"
    
    def action(self, cmd, text):
        self.actIfInterested(".*(time)(?!\\w+).*", cmd, text)   #what time is it
        self.actIfInterested(".*(CMRQ-[0-9]+).*", cmd, text)    #CMRQ-1500
    
        