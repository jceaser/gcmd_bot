
from b_bot import BBot
from rand_str import RandomString

import datetime

class BTime(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.responses = RandomString([
            "It is now"
            , "The current time is"
            , "If you would just look at the clock you would see that it is"
            , ""
        ])
    
    def action(self, cmd, data, found):
        return "%s %s" % (self.responses.pick(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))