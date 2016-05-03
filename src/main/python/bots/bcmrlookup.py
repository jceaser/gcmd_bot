import json
import urllib
import urllib2
import sys
import datetime

from BBot import BBot


#cmrCollectionsByPage = "https://cmr.earthdata.nasa.gov/search/collections.umm-json?%s=%s&page_size=%s&pretty=true"
cmrCollections = "https://cmr.earthdata.nasa.gov/search/collections?%s=%s&pretty=true"
cmrConcepts = "https://cmr.earthdata.nasa.gov/search/concepts/%s?pretty=true"
#cmrConceptRevisions = "https://cmr.earthdata.nasa.gov/search/concepts/%s/%s"

class BCmrLookup(BBot):
    def __init__(self):
        BBot.__init__(self)
    
    def cmrLookup (self, url):
        found = False
        data = None
        try:
            response = urllib2.urlopen(url)
            data = response.read()
            hit = response.info().getheader('CMR-Hits')
            if hit is None or  0<int(hit):
                # we got a 200 and there is no hit value, or the value is > 0
                found = True
        except urllib2.URLError, e:
            found = False
        except urllib2.HTTPError, e:
            found = False
        return found, data
    
    def action(self, cmd, text):
        global cmrCollections
        global cmrConcepts
        
        ''' text should be an id '''
        url = cmrConcepts % (text)
        found, data = self.cmrLookup(url)
        if found:
            msg = cgi.escape(data)
        else:
            url = cmrCollections % ("entry_id", text)
            found, data = self.cmrLookup(url)
            if found:
                msg = cgi.escape(data)
            else:
                url = cmrCollections % ("short_name", text)
                found, data = self.cmrLookup(url)
        if found:
            msg = url
