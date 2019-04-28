import requests
from app import SMARTHOMESERVER_ERROR
import logging


def check_password(webhook_url, password):
    try:
        r = requests.get(webhook_url + '/check_password', params={'password': password}).json()
        logging.debug('Check password return')
        logging.debug(str(r))
        return r['ok']
    except Exception:
        logging.debug('Connection refused')
        return SMARTHOMESERVER_ERROR


def check_webhook(webhook_url):
    try:
        r = requests.get(webhook_url + '/iswebhook').json()
        logging.debug('Check webhook return')
        logging.debug(str(r))
        return r['ok']
    except Exception:
        logging.debug('Connection refused')
        return SMARTHOMESERVER_ERROR


def function(webhook_url, webhook_password, device_id, action):
    try:
        r = requests.get(
            webhook_url + '/action', params={'password': webhook_password, 'action': action, 'device_id': device_id}
        ).json()
        return r
    except Exception:
        logging.debug('Connection refused')
        return SMARTHOMESERVER_ERROR
