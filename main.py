import argparse
import urllib.parse
import urllib.request
import json
import sys
ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush'


def doRequest(args):
    filteredParams = {k: v for k, v in vars(args).items() if v is not None}
    if filteredParams['deviceNames']:
        filteredParams['deviceNames'] = ','.join(filteredParams['deviceNames'])
    filteredParams['apikey'] = getConfig()['apikey']
    url = makeRequestUrl(filteredParams)
    # print(url)
    req = urllib.request.urlopen(url)
    response = json.load(req)
    if (response['success']):
        print("Success!")
        sys.exit(0)
    else:
        errorMessage = response['errorMessage']
        print('Error: ' + errorMessage)
        if errorMessage == 'User Not Authenticated':
            print("--> You should update your API key by running join-cli --setup")
        sys.exit(1)


def makeRequestUrl(params):
    url_parts = list(urllib.parse.urlparse(ENDPOINT))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)

def getConfig():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config

def setConfig(apikey):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump({'apikey': apikey}, f, ensure_ascii=False, indent=4)
        print("Saved!")

def setup():
    print("--> Open this link: https://joinjoaomgcd.appspot.com/")
    print("--> Select \"Join API\"")
    print("--> Click the orange button that says \"SHOW\"")
    print("--> Copy that key…")
    apikey = input("--> …and paste it here: ")
    setConfig(apikey)


parser = argparse.ArgumentParser(description='Process some integers.')
subparsers = parser.add_subparsers()
setup_p = subparsers.add_parser('setup')
# setup_p.add_argument("name")
# setup_p.add_argument("--web_port")

parser.add_argument('--setup', action='store_true')

parser.add_argument("-n", "--device-names", dest="deviceNames", nargs='*', help="device names, separated by comma")
parser.add_argument("--callnumber", help="sets the callnumber")
parser.add_argument("--clipboard", help="sets the clipboard")
parser.add_argument("--text", help="sets the text")
parser.add_argument("--title", help="sets the title")
parser.add_argument("--url", help="sets the url")

args = parser.parse_args()

if args.setup:
    setup()
else:
    doRequest(args)
