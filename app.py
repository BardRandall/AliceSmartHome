from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/alicehome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asjdbasidgausg7di73q783fad7fde'
db = SQLAlchemy(app)
app.config.from_object(__name__)

with open('types.json') as f:
    config = json.load(f)
