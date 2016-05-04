import json
import urllib
import urllib2
import sys
import datetime

from b_bot import BBot

class BBadLang(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.base = "/usr/local/server-data/var"
        self.storage = "bbot_bad_lang.txt"
        self.bad = ["fuck", "shit", "microsoft"]
        
    def action(self, cmd, data):
        msg = None
        text = data[0].text
        
        for word in bad:
            c = text.count(word)
        
        return msg
