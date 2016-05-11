import os, sys, json
import cPickle as pickle
from storage import Storage

class Pickler(Storage):
    
    def __init__(self, config={}):
        '''
        config["path"] should contain the directory of where to read and write
        data to
        '''
        Storage.__init__(self, config)
        if type(config) is dict and config["path"] is not None:
            self.pickle_filepath = config["path"]
        else:
            self.pickle_filepath = "/tmp/pickle.pickle"
    
    def _key(self, name):
        '''
        returns the full path to the data file
        @return data file name
        '''
        return "%s/%s.pickle" % (self.pickle_filepath, name)
    
    def _toType(self, raw):
        '''
        convert to native type if you can, currently dict is supported
        @return Dictionary if posible, string otherwise
        '''
        data = raw
        if type(raw) == type(''):
            if raw.startswith("{") and ":" in raw and raw.endswith("}"):
                clean = str(raw).replace("'", "\"")
                try:
                    parsed = json.loads(clean)
                    data = parsed
                except ValueError, v:
                    print v
                    data = raw
        return data
    
    def _ensureStorage(self):
        ''' initilizes the storage system if need be '''
        if not os.path.exists(self.pickle_filepath):
            os.makedirs(self.pickle_filepath)
    
    def load(self, name):
        '''
        Restores data from the storage system
        @param name value key
        @return data value, dictionary if posible
        '''
        value = None
        key = self._key(name)
        if os.path.exists(key):
            with open(key, 'r') as pickle_handle:
                result = pickle.load(pickle_handle)
                pickle_handle.close()
                value = result
        return value
    
    def store(self, name, value):
        '''
        Stores data to the storage system
        @param name key to save value to
        @param value data to be saved
        '''
        key = self._key(name)
        self._ensureStorage()
        with open(key, 'w') as pickle_handle:
            pickle.dump(value, pickle_handle)
            pickle_handle.close()

def main(argv):
    print "%s %s" % (os.getcwd(), argv[0])
    if len(argv)<1 or argv[0] == "--test":
        pick = Pickler({"path":"./test.file"})
        send = {'first':'thomas', 'last':'cherry'}
        pick.store("one", send)
        receive = pick.load("one")
        print send['first'] == receive['first']
    else:
        pickler = None
        key = None
        
        if len(argv)==1 and argv[0] == "--help":
            print "cmd <path> [key] [value]"
        
        if 1<=len(argv):
            location = argv[0]
            pickler = Pickler(location)
        if 2<=len(argv):
            key = argv[1]
        if 3<=len(argv):
            #at this point we know it is a write
            value = argv[2]
            value = pickler._toType(value)
            pickler.store(key, value)
        elif key is not None:
            #not a write, so lets try doing a read
            value = pickler.load(key)
            print value
        
if __name__ == "__main__": main(sys.argv[1:])
