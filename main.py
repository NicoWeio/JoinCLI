import argparse
import urllib.parse
import urllib.request
import json
import sys
APIKEY = '***REMOVED***'
ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush'


def doRequest(args):
    filteredParams = {k: v for k, v in vars(args).items() if v is not None}
    filteredParams['apikey'] = APIKEY
    url = makeRequestUrl(filteredParams)
    req = urllib.request.urlopen(url)
    response = json.load(req)
    if (response['success']):
        print("Success!")
    else:
        print("Failure!")
        print(response['errorMessage'])


def makeRequestUrl(params):

    url_parts = list(urllib.parse.urlparse(ENDPOINT))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument("-n", "--device-names", dest="deviceNames", help="device names, separated by comma")
parser.add_argument("--callnumber", help="sets the callnumber")
parser.add_argument("--clipboard", help="sets the clipboard")
parser.add_argument("--text", help="sets the text")
parser.add_argument("--title", help="sets the title")
parser.add_argument("--url", help="sets the url")

args = parser.parse_args()

# makeRequestUrl()
doRequest(args)
