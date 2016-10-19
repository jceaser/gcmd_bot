import sys, math
import urllib
import urllib2

from b_bot import BBot

class BDown(BBot):
    def __init__(self):
        BBot.__init__(self)
    
    def get(self, url):
        response = urllib2.urlopen(url, timeout=2)
        response.addheaders = [('User-agent', 'GCMD-Bot')]
        data = response.read()
        return data
    def action(self, cmd, data, found):
       return str(self.get(found.group(1)))

def main(argv):
    bt = BDown()
    print bt.get(argv[0])

if __name__ == "__main__": main(sys.argv[1:])
