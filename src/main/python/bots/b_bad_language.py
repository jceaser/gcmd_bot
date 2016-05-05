import json
import urllib
import urllib2
import sys
import datetime

from b_bot import BBot
from rand_str import RandomString

class BBadLang(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.base = "/usr/local/server-data/var"
        self.storage = "bbot_bad_lang.txt"
        self.bad = ["fuck", "shit", "microsoft"]
        self.responses = RandomString(
            ["Watch the language"
            , "Someone is getting saucy"
            , "Having a bad day?"
            , "I have nothing to say about that"
            , "I wish my programmers would let me say that."
            ])
        
    def action(self, cmd, data, found):
        msg = None
        text = data[0]['text']
        c = 0
        for word in self.bad:
            c = c +  text.count(word)
        
        if 0<c: msg = "\"%s\" - %s" % (text, self.responses.pick())
        return msg
