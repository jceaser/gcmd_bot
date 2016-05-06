import json
import urllib
import urllib2
import sys
import datetime

from b_bot import BBot
from rand_str import RandomString

#cmrCollectionsByPage = "https://cmr.earthdata.nasa.gov/search/collections.umm-json?%s=%s&page_size=%s&pretty=true"
cmrCollections = "https://cmr.%searthdata.nasa.gov/search/collections?%s=%s&pretty=true"
cmrConcepts = "https://cmr.%searthdata.nasa.gov/search/concepts/%s?pretty=true"
#cmrConceptRevisions = "https://cmr.earthdata.nasa.gov/search/concepts/%s/%s"

class BCmrLookup(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.responses = RandomString([
            "I found a record in CMR matching that id:"
            , "That reminds me of someting the CMR server told me the other day:"
            , "Looks like you were talking about a CMR ID so I went a head and looked them up for you:"
            , "You mean you don't know the full URL?"
        ])
        self.multiple_responses = RandomString([
            "I found records in CMR matching that id:"
            , "That reminds me of someting the CMR server told me the other day:"
            , "Looks like you were talking about some CMR IDs so I went a head and looked them up for you:"
            , "You mean you don't know the full URLs?"
        ])
    
    def cmrLookup (self, url):
        found = False
        data = None
        try:
            #print url
            response = urllib2.urlopen(url, timeout=2)
            response.addheaders = [('User-agent', 'GCMD-Bot')]
            data = response.read()
            hit = response.info().getheader('CMR-Hits')
            if hit is None or  0<int(hit):
                # we got a 200 and there is no hit value, or the value is > 0
                found = True
        except urllib2.URLError, e:
            found = False
            data = None
        except urllib2.HTTPError, e:
            print e.code
            found = False
            data = None
        return found, data
    
    def find(self, cmd, data, found):
        global cmrCollections
        global cmrConcepts
        
        text = found.group(1)
        msg = []
        found = False
        
        for env in ["", "uat.", "sit."]:
            ''' text should be an id '''
            
            url = cmrConcepts % (env, text)
            found, data = self.cmrLookup(url)
            if found:
                msg.append(url)
                if cmd is not "cmr_all":
                    break
            
            url = cmrCollections % (env, "entry_id", text)
            found, data = self.cmrLookup(url)
            if found:
                msg.append(url)
                if cmd is not "cmr_all":
                    break
                
            url = cmrCollections % (env, "short_name", text)
            found, data = self.cmrLookup(url)
            if found:
                msg.append(url)
                if cmd is not "cmr_all":
                    break
        return msg

    def action(self, cmd, data, found):
        msg = None
        urls = self.find(cmd, data, found)
        if 0<len(urls):
            text_urls = "\n".join(urls)
            r = self.multiple_responses if cmd=="cmr_all" else self.responses
            msg = "%s\n%s" % (r.pick(), text_urls)
        return msg

def main(argv):
    cl = BCmrLookup()
    print cl.action(None, {u'text': u'testing find: msut2', u'ts': u'1462474491.000084', u'user': u'U13SD9KSN', u'team': u'T13S7BSJD', u'type': u'message', u'channel': u'C14FTCSKV'}, "msut2")

if __name__ == "__main__": main(sys.argv[1:])
