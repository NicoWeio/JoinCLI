import argparse
import urllib.parse
import urllib.request
import json
import sys
APIKEY = '***REMOVED***'
ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush'


def doRequest(args):
    print(args)
    #TODO 'callnumber':args.callnumber
    params = {'apikey': APIKEY, 'deviceNames': args.device_names, 'text': args.text, 'url':args.url}
    # print(params)

    url = makeRequestUrl(params)
    print(url)
    f = urllib.request.urlopen(url)
    response = json.load(f)
    print(response)
    if (response['success']):
        print("Success!")
    else:
        print("Failure!")
        print(response)




def makeRequestUrl(params):

    url_parts = list(urllib.parse.urlparse(ENDPOINT))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)


parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--device-id', dest='accumulate', action='store_const',
#                     const=sum, help='sum the integers (default: find the max)')
# parser.add_argument('--title', dest='accumulate', action='store_const',
#                     const=title, help='sets the title')
parser.add_argument("-n", "--device-names", help="device names, separated by comma")
parser.add_argument("--callnumber", help="sets the callnumber")
parser.add_argument("--text", help="sets the text")
parser.add_argument("--title", help="sets the title")
parser.add_argument("--url", help="sets the url")

args = parser.parse_args()

# makeRequestUrl()
doRequest(args)
