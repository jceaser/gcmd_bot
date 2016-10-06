
from b_bot import BBot
from rand_str import RandomString
from storage.pickle import Pickler

import datetime

DEF_SLACK_BOT_STORAGE = "/tmp/slack_bot"

class BRemember(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.pickle_jar = Pickler("/tmp/slack_bot")
        self.responses = RandomString([
            "Storing value."
            , "I will remember that allways."
            , "If you think it is important, then I will remember it."
            , "Done"
        ])
    
    def action(self, cmd, data, found):
        self.pickle_jar.store(found.group(1), found.group(2))
        return "%s '%s'='%s'\n%s" % (self.responses.pick(), found.group(1), found.group(2), "saved")
        
class BRecall(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.pickle_jar = Pickler("/tmp/slack_bot")
        self.responses = RandomString([
            "I remember you telling me..."
            , "Do you remember..."
        ])
    
    def action(self, cmd, data, found):
        return "%s @'%s'\n%s" % (self.responses.pick(), found.group(1), self.pickle_jar.load(found.group(1)))