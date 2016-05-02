from BTime import *

import re

class BBots:
    
    def actIfInterested(self, interest, cmd, text):
        handler = None
        m = re.search(interest, text)
        if m is not None:
            #print "group='%s'." % m.group(0)
            handler = BTime()
        
        if handler is not None:
            print handler.action(cmd, text)
        else:
            print "no handler found"
    
    def action(self, cmd, text):
        self.actIfInterested(".*(time)(?!\\w+).*", cmd, text)
    
        