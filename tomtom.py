import urllib2
import json

"""
TRAFFIC INFORMATION
===================
"""

work = 'http://routes.tomtom.com/lbs/services/route/1/37.786194,-122.39897:37.33233,-122.03073/Quickest/json/1e2099c7-eea9-476b-a\
ac9-b20dc7100af1;language=en;avoidTraffic=true;includeTraffic=true;day=today;time=now;iqRoutes=2;trafficModelId=1358732719560;map=basic'
home = 'http://routes.tomtom.com/lbs/services/route/1/37.33233,-122.03073:37.786194,-122.39897/Quickest/json/1e2099c7-eea9-476b-aac9-b20dc7100af1;language=en;avoidTraffic=true;includeTraffic=true;day=today;time=now;iqRoutes=2;trafficModelId=1358732719560;map=basic'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.27 (KHTML, like Gecko) Chrome/26.0.1386.0 Safari/537.27'


def getDelay(url):
    """
    Desc: Returns the delay time in seconds for the route to san francisco.
    Args:
      url = this is the routes url api reques
    """
    request = urllib2.Request(url)
    request.add_header('User-Agent', user_agent)
    request.add_header('Referer', 'http://routes.tomtom.com/')
    response = urllib2.urlopen(request)
    r = response.read()
    return json.loads(r)['route']['summary']['totalDelaySeconds']

def traffic(where):
    if where == 'home':
        return getDelay(home)
    if where == 'work':
        return getDelay(work)


