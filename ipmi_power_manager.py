import argparse
import logging
import os

import requests
import urllib3
from dotenv import load_dotenv

logger = logging.getLogger("__name__")
logging.basicConfig(
        format="%(asctime)s [%(levelname)8s] [%(name)s:%(lineno)s:%(funcName)20s()] --- %(message)s",
        level=logging.INFO,
    )
logging.getLogger("urllib3").setLevel(logging.WARNING)
urllib3.disable_warnings()

load_dotenv()

IPMI_USERNAME = os.getenv("IPMI_USERNAME")
IPMI_PASSWORD = os.getenv("IPMI_PASSWORD")

API_ROOT = "https://spmaxi-ipmi.home.devmem.ru/redfish/v1/"
API_AUTH = "SessionService/Sessions"
API_ACTIONS_RESET = "Systems/1/Actions/ComputerSystem.Reset"

POWER_STATE_ON = "On"
POWER_STATE_OFF = "GracefulShutdown"

parser = argparse.ArgumentParser(description="Supermicro IPMI Power Manager")
parser.add_argument("--on", dest="power_state", action="store_true")
parser.add_argument("--off", dest="power_state", action="store_false")
args = parser.parse_args()

if args.power_state:
    power_state = POWER_STATE_ON
else:
    power_state = POWER_STATE_OFF


def get_auth_headers():
    logger.debug("Get session headers")
    endpoint_url = API_ROOT + API_AUTH
    payload = f'{{"UserName": "{IPMI_USERNAME}","Password": "{IPMI_PASSWORD}"}}'
    headers = {"Content-Type": "application/json"}

    r = requests.post(endpoint_url, headers=headers, data=payload, verify=False)
    return r.headers


def set_power_state(value):
    logger.debug("Set power state to '%s'", value)
    endpoint_url = API_ROOT + API_ACTIONS_RESET
    payload = f'{{"ResetType": "{value}"}}'
    headers = get_auth_headers()

    r = requests.post(endpoint_url, headers=headers, data=payload, verify=False)
    print(r.json())


set_power_state(power_state)
