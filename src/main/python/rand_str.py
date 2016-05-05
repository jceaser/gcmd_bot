import sys
from random import randint

class RandomString:
    ''' Store strings and randomly deliver them '''
    def __init__(self, list=None):
        '''
        @param list allow for an optional initial list of values
        '''
        self.list = [] if list == None else list
    def add(self, text):
        '''
        @param text string to randomly deliver, adds to internal list
        '''
        self.list.append(text)
    def pick(self):
        '''
        @return one of the supplied strings, randomly selected
        '''
        return self.list[randint(0,len(self.list)-1)]

def unit():
    ''' Unit test the object, count distribution across three values '''
    rs = RandomString(["high", "medium", "low"])
    counts = {}
    for i in range(0xffff):
        text = rs.pick()
        if text in counts:
            counts[text] = int(counts[text]) + 1
        else:
            counts[text] = 1
    print "counts by value: %s" % counts

def main(argv):
    '''
    @param argv list of strings, if none then unit test
    '''
    if 0==len(argv):
        unit()
        return
    rs = RandomString()
    for arg in argv:
        if arg.startswith("-"):
            pass
        else:
            rs.add(arg)
    print rs.pick()

if __name__ == "__main__": main(sys.argv[1:])
