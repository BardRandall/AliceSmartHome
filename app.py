from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
SMARTHOMESERVER_ERROR = 202
DEVICE_NOT_FOUND = 203
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://AliceSmartHub:qwerty123@AliceSmartHub.mysql.pythonanywhere-services.com/AliceSmartHub$smarthub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asjdbasidgausg7di73q783fad7fde'
db = SQLAlchemy(app)
app.config.from_object(__name__)

sessionStorage = {}

logging.basicConfig(level=logging.DEBUG, filename='server.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# STATUSES
MAIN_MENU = 0
ENTER_SMARTHOME_WEBHOOK = 1
ENTER_SMARTHOME_PASSWORD = 2
ENTER_NAME = 3
ENTER_DEVICE_ID = 4
ENTER_DEVICE_NAME = 5

