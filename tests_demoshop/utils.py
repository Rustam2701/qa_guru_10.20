import json
import logging
import requests
import allure
from curlify import to_curl

from tests_demoshop.conftest import DOMAIN_URL


def post_demowebshop(url, **kwargs):
    with allure.step(f"POST {url}"):
        response = requests.post(url=DOMAIN_URL, **kwargs)
        curl = to_curl(response.request)
        logging.debug(to_curl(response.request))
        logging.info(f'status code: {response.status_code}')
        allure.attach(body=curl, name="curl", attachment_type=allure.attachment_type.TEXT, extension='txt')
        allure.attach(body=json.dumps(response.json(), indent=4), name="response",
                      attachment_type=allure.attachment_type.JSON, extension='json')
        return response


def get_demowebshop(url, **kwargs):
    with allure.step(f"GET {url}"):
        response = requests.get(url=DOMAIN_URL, **kwargs)
        curl = to_curl(response.request)
        logging.info(to_curl(response.request))
        logging.info(f'status code: {response.status_code}')
        allure.attach(body=curl, name="curl", attachment_type=allure.attachment_type.TEXT, extension='txt')
        allure.attach(body=json.dumps(response.json(), indent=4), name="response",
                      attachment_type=allure.attachment_type.JSON, extension='json')
        return response
