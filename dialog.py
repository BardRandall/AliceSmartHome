from app import db, sessionStorage, ENTER_SMARTHOME_WEBHOOK, ENTER_SMARTHOME_PASSWORD, MAIN_MENU, ENTER_NAME
from Integration import *
import logging
from extra import *


def set_status(session_id, status):
    sessionStorage[session_id]['status'] = status


def old_user_start(**kwargs):
    response = kwargs['response']
    set_main_menu_gui(response)
    logging.info('User logged in<br>')


def new_user_start(**kwargs):
    logging.debug('Kwargs:<br>')
    logging.debug(str(kwargs) + '<br>')
    set_status(kwargs['request']['session']['session_id'], ENTER_NAME)
    logging.info('New user registered<br>')
    response = kwargs['response']
    response['response']['text'] = 'Добро пожаловать в систему умный дом. Назовите свое имя, пожалуйста!'


def no_session(**kwargs):
    response = kwargs['response']
    response['response']['text'] = 'Извините, ваша сессия закончилась. Перезагрузите навык'
    response['response']['end_session'] = True
    logging.warning('Not found user session<br>')


def unexpected_error(**kwargs):
    logging.debug('Kwargs:')
    logging.debug(str(kwargs))
    response = kwargs['response']
    response['response']['text'] = 'Неизвестная ошибка. Перезагрузите навык'
    response['response']['end_session'] = True
    logging.error('Unexpected error: {}<br>'.format(str(kwargs['error'])))


def main_menu(**kwargs):
    response = kwargs['response']
    response['response']['text'] = 'Main menu'
    response['response']['end_session'] = True
    logging.warning('Not found user session<br>')


def enter_name(**kwargs):
    request = kwargs['request']
    response = kwargs['response']
    session_id = request['session']['session_id']
    name = get_first_name(request)
    if name is None:
        response['response']['text'] = 'Я не расслышала имя. Повторите еще раз'
    else:
        sessionStorage[request['session']['session_id']]['name'] = name[0].upper() + name[1:].lower()
        logging.info('User set name')
        set_status(request['session']['session_id'], ENTER_SMARTHOME_WEBHOOK)
        response['response']['text'] = 'Хорошо, {}. Теперь введите URL вашего сервера'.format(sessionStorage[session_id]['name'])


def enter_smarthome_webhook(**kwargs):
    webhook = kwargs['request']['request']['original_utterance']
    response = kwargs['response']
    session_id = kwargs['request']['session']['session_id']
    res = check_webhook(webhook)
    if type(res) != bool or not res:
        response['response']['text'] = 'Проверьте Webhook URL и повторите попытку'
    else:
        sessionStorage[session_id]['webhook_url'] = webhook
        set_status(session_id, ENTER_SMARTHOME_PASSWORD)
        response['response']['text'] = 'Введите пароль от сервера, {}'.format(sessionStorage[session_id]['name'])


def set_main_menu_gui(response):
    response['response']['text'] = 'Главное меню'


def enter_smarthome_password(**kwargs):
    password = kwargs['request']['request']['original_utterance']
    response = kwargs['response']
    session_id = kwargs['request']['session']['session_id']
    res = check_password(sessionStorage[session_id]['webhook_url'], password)
    if type(res) != bool or not res:
        response['response']['text'] = 'Проверьте пароль Webhook и повторите попытку'
    else:
        user = User(name=sessionStorage[session_id]['name'], user_id=kwargs['request']['session']['user_id'])
        sh = SmartHome(webhook_url=sessionStorage[session_id]['webhook_url'], password=password, user=user)
        db.session.add(user)
        db.session.add(sh)
        db.session.commit()
        set_status(session_id, MAIN_MENU)
        set_main_menu_gui(response)


status_handle = {
    ENTER_SMARTHOME_WEBHOOK: enter_smarthome_webhook,
    ENTER_SMARTHOME_PASSWORD: enter_smarthome_password,
    MAIN_MENU: main_menu,
    ENTER_NAME: enter_name
}