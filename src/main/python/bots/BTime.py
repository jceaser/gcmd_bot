
#from BBot import *
from BBot import BBot

import datetime

class BTime(BBot):
    def __init__(self):
        BBot.__init__(self)
    
    def action(self, cmd, text):
       return "hello world from %s: %s -> %s" % (cmd, text, datetime.datetime.now())