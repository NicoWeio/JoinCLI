#!/usr/bin/python3

import argparse
import urllib.parse
import urllib.request
import json
import sys
import os
from pathlib import Path
PUSH_ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush'
LIST_DEVICES_ENDPOINT = 'https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices'
# FILE_UPLOAD_ENDPOINT = 'https://transfer.sh'
# FILE_UPLOAD_ENDPOINT = 'https://file.io'
FILE_UPLOAD_ENDPOINT = 'https://0x0.st/'
# FILE_UPLOAD_ENDPOINT = 'http://httpbin.org/post'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def doRequest(args):
    filteredParams = {k: v for k, v in vars(args).items() if v is not None}
    if 'deviceNames' in filteredParams:
        filteredParams['deviceNames'] = ','.join(filteredParams['deviceNames'])
    filteredParams['apikey'] = getConfig()['apikey']
    result = doActualRequest(PUSH_ENDPOINT, filteredParams)
    if result:
        print(f"{bcolors.OKGREEN}Pushed successfully!{bcolors.ENDC}")
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
        print(f"{bcolors.FAIL}Error: " + errorMessage + bcolors.ENDC)
        if errorMessage == 'User Not Authenticated':
            print("--> You should update your API key by running join-cli setup")
        sys.exit(1)


def testApiKey(key):
    url = makeRequestUrl(LIST_DEVICES_ENDPOINT, {
        'apikey': key})
    req = urllib.request.urlopen(url)
    response = json.load(req)
    return ('success' in response) and response['success']


def makeRequestUrl(endpoint, params):
    url_parts = list(urllib.parse.urlparse(endpoint))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


def getDevices():
    r = doActualRequest(LIST_DEVICES_ENDPOINT, {
                        'apikey': getConfig()['apikey']})
    return r['records']


def getConfigPath():
    home = str(Path.home())
    return os.path.join(home, '.join-cli-config.json')


def getConfig():
    with open(getConfigPath(), 'r') as f:
        config = json.load(f)
        return config


def setConfig(config):
    with open(getConfigPath(), 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def updateConfig(key, value):
    try:
        config = getConfig()
        config[key] = value
        setConfig(config)
    except FileNotFoundError as e:
        print(f"{bcolors.OKBLUE}Config file not found. It will be created here: {getConfigPath()}{bcolors.ENDC}")
        setConfig({key: value})
    print(f"{bcolors.OKBLUE}Updated " + key + f" in config{bcolors.ENDC}")


def setup():
    print("--> Open this link: https://joinjoaomgcd.appspot.com/")
    print("--> Select \"Join API\"")
    print("--> Click the orange button that says \"SHOW\"")
    print("--> Copy that key…")
    apikey = input("--> …and paste it here (leave empty to abort): ")
    if apikey:
        if testApiKey(apikey):
            updateConfig('apikey', apikey)
        else:
            print(
                f"{bcolors.FAIL}That did not work. The key you entered appears to be invalid.{bcolors.ENDC}")
    else:
        print("Aborted.")


def uploadFile(path):
    import requests  # TODO grmbl…
    filename = os.path.basename(path)
    with open(path, 'rb') as f:
        r = requests.post(FILE_UPLOAD_ENDPOINT,
                          files=dict(file=open(path, 'rb')))
        fileurl = r.text.strip('\n')
        print(f"{bcolors.OKBLUE}Upload complete! URL: "
              + fileurl + bcolors.ENDC)
        return r.text.strip('\n')


parser = argparse.ArgumentParser(
    description="Send pushes via joaomgcd's Join API")
subparsers = parser.add_subparsers(dest='command')

setup_p = subparsers.add_parser('setup')
setup_p.add_argument("--update-devices", action="store_true")
setup_p.add_argument("--set-default-devices", action="store_true")

parser.add_argument('--list-devices', action='store_true')

push_p = subparsers.add_parser('push')
push_p.add_argument("-d", "--device-names", dest="deviceNames",
                    nargs='*', help="device names, separated by comma")
push_p.add_argument("--callnumber", help="sets the callnumber")
push_p.add_argument("--clipboard", help="sets the clipboard")
push_p.add_argument("-t", "--text", help="sets the text")
push_p.add_argument("--title", help="sets the title")
push_p.add_argument("-u", "--url", help="sets the url")
push_p.add_argument("-f", "--local-file",
                    help="uploads the file to a server and pushes the URL")

args = parser.parse_args()

if args.command == 'setup':
    if args.update_devices:
        devices = getDevices()
        updateConfig('devices', devices)
    elif args.set_default_devices:
        devices = getDevices()
        i = 1
        for dev in devices:
            print("[" + str(i) + "] " + dev['deviceName'])
            i += 1
        devList = input("Choose one or multiple devices, separated by comma: ")
        devIntList = list(map(lambda d: int(d), devList.split(',')))

        resultingDevices = list()
        i = 1
        for dev in devices:
            if i in devIntList:
                resultingDevices.append(dev)
            i += 1
        deviceNameList = list(map(lambda d: d['deviceName'], resultingDevices))
        if not deviceNameList:
            print("No device selected. Aborting.")
        else:
            updateConfig('defaultDeviceNames', deviceNameList)
    else:
        setup()
elif args.list_devices:
    devices = getDevices()
    for dev in devices:
        print(dev['deviceName'])
elif args.command == 'push':
    if args.local_file:
        url = uploadFile(args.local_file)
        args.file = url

    doRequest(args)
else:
    parser.print_help()
