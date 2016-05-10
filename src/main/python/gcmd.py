#!/usr/bin/python
import cgi
import cgitb #; cgitb.enable()  # for troubleshooting
import os, sys

import urllib, urllib2

from bots.b_bots import BBots

'''
A slack command responder

j or jira <bugid>
g or get <url>
c or cmr <url>
'''

if 'GATEWAY_INTERFACE' in os.environ:
    cgitb.enable()
#else:
#    print ('Not CGI. CLI')

cmrCollectionsByPage = "https://cmr.earthdata.nasa.gov/search/collections.umm-json?%s=%s&page_size=%s&pretty=true"
cmrCollections = "https://cmr.earthdata.nasa.gov/search/collections?%s=%s&pretty=true"
cmrConcepts = "https://cmr.earthdata.nasa.gov/search/concepts/%s?pretty=true"
cmrConceptRevisions = "https://cmr.earthdata.nasa.gov/search/concepts/%s/%s"

def cmd_main(argv):
    process("toolbot", " ".join(argv))

def cgi_main():
    form = cgi.FieldStorage()
    command = form.getvalue("command", "")
    if command.startswith("/"):
        command = command[1:]
    text = urllib.unquote(form.getvalue("text", ""))
    msg = ""
    process(command, text)

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
    msg = ""
    bots = BBots()
    
    if command is None or command == "":
        msg = "Hello World"
    elif command == "?" or command == "help":
        template = "%s* %s %-10s - %s\n"
        msg = "Commands:\n"
        msg = template % (msg, "?", "help", "this message")
        msg = template % (msg, "j", "jira [bug]", "url to jira")
        msg = template % (msg, "c", "cmr [id]", "url to cmr")
        msg = template % (msg, "h", "hangout", "url to hangout")
    elif command == "j" or command == "jira":
        msg = "https://bugs.earthdata.nasa.gov/browse/%s" % text
    elif command == "c" or command == "cmr" or command == "cmr-prod":
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
    elif command == "h" or command == "hangout":
        msg = "https://hangouts.google.com/start"
    elif command == "t" or command == "toolbot":
        ##recursive
        #list = text.split()
        #if 0<len(list):
        #    process(list[0], "")
        #elif 1<len(list):
        #    process(list[0], " ".join(list[1:]))
        #return
        
        msg = bots.action(text)
    
    page (msg)

def page(msg):
    print "Content-Type: text/html"
    print ""
    if msg is None:
        print "No respones"
    else:
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
    print "----"
    process("toolbot", "cmr msut2_5")
    print "----"
    process("toolbot", "c msut2_5")
    print "----"
    process("toolbot", "hangout")
    print "----"
    process("toolbot", "help")

if 'GATEWAY_INTERFACE' in os.environ:
    cgi_main()
elif __name__ == "__main__":
    if sys.argv[1] == "--test":
        test()
    else:
        cmd_main(sys.argv[1:])
