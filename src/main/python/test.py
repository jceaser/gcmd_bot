from bots.BTime import BTime
from bots.BBots import BBots
#import bots.BBots


bt = BTime()
print bt.action("command", "text")

bots = BBots()
bots.action("time", "now")
bots.action("time", "timestamp")
bots.action("time", "tell me the time")
bots.action("time", "what time is it")
bots.action("time", "time as of now?")

print "----"

bots.action("cmr", "CMRQ-1500");

print