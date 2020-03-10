import argparse
import urllib.parse
import urllib.request
APIKEY = '***REMOVED***'
ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush'


def doRequest(devNames, text):
    params = {'apikey': APIKEY, 'deviceNames': devNames, 'text': text}

    url = makeRequestUrl(params)
    print(url)
    f = urllib.request.urlopen(url)
    print(f.read().decode('utf-8'))


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
parser.add_argument("-n", "--dev-names", help="device names, separated by comma")
parser.add_argument("--text", help="sets the text")
parser.add_argument("--title", help="sets the title")

args = parser.parse_args()

# makeRequestUrl()
doRequest(devNames=args.dev_names, text=args.text)
