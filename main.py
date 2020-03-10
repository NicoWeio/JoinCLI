import argparse
import urllib.parse
import urllib.request
import json
import sys
PUSH_ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush'
LIST_DEVICES_ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices'


def doRequest(args):
    filteredParams = {k: v for k, v in vars(args).items() if v is not None}
    if filteredParams['deviceNames']:
        filteredParams['deviceNames'] = ','.join(filteredParams['deviceNames'])
    filteredParams['apikey'] = getConfig()['apikey']
    result = doActualRequest(PUSH_ENDPOINT, filteredParams)
    if result:
        print("Pushed successfully!")
        sys.exit(0)


def doActualRequest(endpoint, params):
    url = makeRequestUrl(endpoint, params)
    # print(url)
    req = urllib.request.urlopen(url)
    response = json.load(req)
    if (response['success']):
        return response
    else:
        errorMessage = response['errorMessage']
        print('Error: ' + errorMessage)
        if errorMessage == 'User Not Authenticated':
            print("--> You should update your API key by running join-cli --setup")
        sys.exit(1)


def makeRequestUrl(endpoint, params):
    url_parts = list(urllib.parse.urlparse(endpoint))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


def getDevices():
    r = doActualRequest(LIST_DEVICES_ENDPOINT, {'apikey': getConfig()['apikey']})
    return r['records']


def getConfig():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config

def setConfig(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
        print("Saved!")

def updateConfig(key, value):
    config = getConfig()
    config[key] = value
    setConfig(config)


def setup():
    print("--> Open this link: https://joinjoaomgcd.appspot.com/")
    print("--> Select \"Join API\"")
    print("--> Click the orange button that says \"SHOW\"")
    print("--> Copy that key…")
    apikey = input("--> …and paste it here: ")
    setConfig({'apikey': apikey})


parser = argparse.ArgumentParser(description='Process some integers.')
subparsers = parser.add_subparsers(dest='command')
setup_p = subparsers.add_parser('setup')
# setup_p.add_argument("name")
setup_p.add_argument("--update-devices", action="store_true")

# parser.add_argument('--setup', action='store_true')
parser.add_argument('--list-devices', action='store_true')

parser.add_argument("-n", "--device-names", dest="deviceNames",
                    nargs='*', help="device names, separated by comma")
parser.add_argument("--callnumber", help="sets the callnumber")
parser.add_argument("--clipboard", help="sets the clipboard")
parser.add_argument("--text", help="sets the text")
parser.add_argument("--title", help="sets the title")
parser.add_argument("--url", help="sets the url")

args = parser.parse_args()

if args.command == 'setup':
    if args.update_devices:
        devices = getDevices()
        updateConfig('devices', devices)
    else:
        setup()
elif args.list_devices:
    devs = getDevices()
    for dev in devs:
        print(dev['deviceName'])
else:
    doRequest(args)
