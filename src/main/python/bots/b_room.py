
from b_bot import BBot
from rand_str import RandomString

import datetime

class BRoom(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.mode = "room"
        self.responses = RandomString([
            "A room for you"
            , "Talk it out here -> "
            , "Click this link to open a room"
            , "Another auto generated smoke filled cloke room: "
            , "A shiny new room for you: "
        ])
    def service(self, mode):
        self.mode = mode
    def action(self, cmd, data, found):
        #https://room.co/#/Slack-MwTyxMrDQtwTUlEM
        #https://hangouts.google.com/start
        
        if self.mode=="room":
            url = "%s https://room.co/#/Slack-%s-%s-%s" % (self.responses.pick(), data["team"], data["channel"], datetime.datetime.now().strftime("%Y-%m-%d_%H_%M"))
        elif self.mode=="hangout":
            url = "https://hangouts.google.com/start"
        #else:
        #    url = None
        
        return url