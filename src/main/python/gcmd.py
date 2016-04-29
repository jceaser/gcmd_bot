#!/usr/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

import urllib2

'''
j or jira <bugid>
g or get <url>
c or cmr <url>
'''

# C10000000-AAAAAA
cmrCollectionsByPage = "https://cmr.earthdata.nasa.gov/search/collections.umm-json?%s=%s&page_size=%s&pretty=true"
cmrCollections = "https://cmr.earthdata.nasa.gov/search/collections?%s=%s&pretty=true"
cmrConcepts = "https://cmr.earthdata.nasa.gov/search/concepts/%s?pretty=true"
cmrConceptRevisions = "https://cmr.earthdata.nasa.gov/search/concepts/%s/%s"

form = cgi.FieldStorage()
command = form.getvalue("command", "")
text = form.getvalue("text", "")
msg = ""

def cmrLookup (url):
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

def process(command, text):
    global msg
    global cmrCollections
    global cmrConcepts
    if command is None or command is "":
        msg = "Hello World"
    elif command is "j" or command is "jira":
        msg = "https://bugs.earthdata.nasa.gov/browse/%s" % text
    elif command is "c" or command is "cmr" or command is "cmr-prod":
        ''' text should be an id '''
        url = cmrConcepts % (text)
        found, data = cmrLookup(url)
        if found:
            msg = cgi.escape(data)
        else:
            url = cmrCollections % ("entry_id", text)
            found, data = cmrLookup(url)
            if found:
                msg = cgi.escape(data)
            else:
                url = cmrCollections % ("short_name", text)
                found, data = cmrLookup(url)
        if found:
            msg = url
    page (msg)

def page(msg):
    print "Content-type: text/plain"
    print "%s" % (cgi.escape(msg))

def test():
    process("", "")
    print "----"
    process("jira", "CMRQ-1500")
    print "----"
    process("cmr", "C169880-GHRC")
    print "----"
    process("cmr", "C169880-GHRC/35")
    print "----"
    process("cmr", "msut2")
    print "----"
    process("cmr", "msut2_5")

#test()