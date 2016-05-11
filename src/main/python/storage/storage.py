#import os, sys
#import cPickle as pickle

#pickle_filepath = "/Users/tacherr1/Documents/picklefile.pickle"

class Storage:
    def __init__(self, config={}):
        self.version = 0.1
        self.config = config
    def load(self, name):
        raise NotImplementedError
    def store(self, name, value):
        raise NotImplementedError
