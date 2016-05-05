
from b_bot import BBot
from rand_str import *

class BJira(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.responses = RandomString(
        [
            "Looks like you were talking about ticket"
            , "You might find that ticket at"
            , "Try"
        ])
    
    def action(self, cmd, id, found):
        url = "https://bugs.earthdata.nasa.gov/browse/%s" % found.group(1)
        return "%s %s" % (self.responses.pick(), url)        