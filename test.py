import requests

webhook_url = 'http://92.252.236.5:8080'

try:
    r = requests.get(webhook_url + '/iswebhook').json()
    print(r)
    print(r['ok'])
    print(type(r['ok']))
except Exception:
    print('error')
