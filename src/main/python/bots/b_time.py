
from b_bot import BBot

import datetime

class BTime(BBot):
    def __init__(self):
        BBot.__init__(self)
    
    def action(self, cmd, data):
        return "It is now %s" % (datetime.datetime.now())