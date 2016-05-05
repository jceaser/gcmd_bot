from b_bot import BBot

import urllib

class BEncode(BBot):
    def __init__(self):
        BBot.__init__(self)
    
    def action(self, cmd, data, found):
        return str(urllib.quote(found.group(1).strip()))

class BDecode(BBot):
    def __init__(self):
        BBot.__init__(self)
    
    def action(self, cmd, data, found):
        return str(urllib.unquote(found.group(1).strip()))
