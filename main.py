from app import app
from flask import request
import json
import models


def generate_answer(data):
    return json.dumps(data)


@app.route('/')
def index():
    return 'SmartHomeServer v.1.0'


@app.route('/iswebhook')
def iswebhook():
    return generate_answer({'ok': True})


@app.route('/check_password')
def check_password():
    with open('password.txt') as f:
        password = f.read().rstrip()
    if request.args.get('password') != password:
        return generate_answer({'ok': False})
    return generate_answer({'ok': True})


#app.run(host='192.168.1.238', port=80, debug=True)
app.run(host='127.0.0.1', port=8080)
