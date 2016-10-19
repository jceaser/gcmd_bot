import sys, math
import urllib
import urllib2
import json

from b_bot import BBot

class BWeather(BBot):
    def __init__(self):
        BBot.__init__(self)
        self.url = "http://forecast.weather.gov/MapClick.php?lat=39.3421&lon=-76.4452&unit=0&lg=english&FcstType=json"
    
    def get(self, url):
        data = None
        try:
            response = urllib2.urlopen(url, timeout=2)
            response.addheaders = [('User-agent', 'GCMD-Bot')]
            data = response.read()
        except:
            None
        return data
    def get_json(self, url):
        raw = self.get(url)
        data = None
        if raw is not None:
            data = json.loads(raw)
        return data
    def weather(self, data):
        weather = "Could not get weather"
        json = self.get_json(self.url)
        if json is not None:
            data = json["data"]
            time = json["time"]
            name = "Weather"
            if time is not None:
                spn = time["startPeriodName"]
                if spn is not None and 0<len(spn):
                    if 0<len(spn[0]):
                        name = spn[0]
            if data is not None:
                text = data["text"]
                if text is not None and 0<len(text):
                    first = text[0]
                    if first is not None and 0<len(first):
                        weather = "%s > %s" % (name, first)
        return weather

    def action(self, cmd, data, found):
       return str(self.weather(found.group(1)))

def main(argv):
    bt = BWeather()
    print bt.weather(argv[0])

if __name__ == "__main__": main(sys.argv[1:])


#http://forecast.weather.gov/MapClick.php?lat=39.3421&lon=-76.4452&unit=0&lg=english&FcstType=dwml
#http://forecast.weather.gov/MapClick.php?lat=39.3421&lon=-76.4452&unit=0&lg=english&FcstType=kml
#http://forecast.weather.gov/MapClick.php?lat=39.3421&lon=-76.4452&unit=0&lg=english&FcstType=json