import logging
import os

import requests
import urllib3
from dotenv import load_dotenv

logger = logging.getLogger('__name__')
urllib3.disable_warnings()

load_dotenv()

IPMI_USERNAME = os.getenv('IPMI_USERNAME')
IPMI_PASSWORD = os.getenv('IPMI_PASSWORD')

baseuri = 'https://spmaxi-ipmi/redfish/v1/'
category_auth = 'SessionService/Sessions'
category_actions = 'Systems/1/Actions/ComputerSystem.Reset'
auth_header = 'X-Auth-Token'


def get_auth_token():
    payload = F'{{"UserName": "{IPMI_USERNAME}","Password": "{IPMI_PASSWORD}"}}'
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.post(
        baseuri+category_auth,
        headers=headers,
        data=payload,
        verify=False)
    return r.headers[auth_header]


def set_power_on():
    payload = '{"ResetType": "On"}'
    auth_token = get_auth_token()
    headers = {
        auth_header: auth_token,
        'Content-Type': 'application/json'
    }

    r = requests.post(
        baseuri+category_actions,
        headers=headers,
        data=payload,
        verify=False)
    print(r.text.encode('utf8'))


if __name__ == '__main__':
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.basicConfig(
        format='%(asctime)s [%(levelname)8s] [%(name)s:%(lineno)s:%(funcName)20s()] --- %(message)s',
        level=logging.DEBUG)

    set_power_on()
