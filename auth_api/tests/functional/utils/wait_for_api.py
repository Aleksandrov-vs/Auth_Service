import logging
import os
import sys
import time
from http import HTTPStatus

import requests

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import test_settings

if __name__ == '__main__':

    while True:
        try:
            response = requests.get(f'{test_settings.service_url}/hello_world')
            if response.status_code == HTTPStatus.OK:
                print('services is available!!')
                break
        except requests.exceptions.ConnectionError:
            print('api is unavailable. Wait..ю')
        time.sleep(2)
