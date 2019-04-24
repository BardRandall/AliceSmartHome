from app import app, status_handle, sessionStorage
from flask import request
import json
from extra import *
from dialog import new_user_start, old_user_start, no_session, unexpected_error


@app.route('/post', methods=['GET', 'POST'])
def post():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    return json.dumps(response)


@app.route('/console2')
def console():
    with open('server.log', mode='r') as f:
        data = f.read()
    return data


def handle_dialog(request, response):
    try:

        user_id = request['session']['user_id']
        session_id = request['session']['session_id']
        basic_config = {
            'user_id': user_id,
            'response': response,
            'session_id': session_id,
            'request': request
        }

        if request['session']['new']:
            if is_user_exists(request['session']['user_id']):
                old_user_start(**basic_config)
            else:
                new_user_start(**basic_config)
            return
        if session_id not in sessionStorage:
            no_session(**basic_config)
            return
        status_handle[sessionStorage[session_id]['status']](**basic_config)
    except Exception as e:
        unexpected_error(error=e)


app.run(host='127.0.0.1', port=8080, debug=True)
