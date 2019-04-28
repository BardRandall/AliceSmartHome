from app import app, config
import json
from flask import request, render_template, session, redirect, url_for
from models import *
from extra import *


def generate_answer(data):
    return json.dumps(data)


def is_authorized():
    if 'authed' in session:
        return session['authed']
    return False


@app.route('/')
def index():
    return 'SmartHomeServer v.1.0'


@app.route('/iswebhook')
def iswebhook():
    return generate_answer({'ok': True})


@app.route('/action')
def action():
    password = request.args['password']
    type = int(request.args['type'])
    device_id = int(request.args['device_id'])
    with open('password.txt') as f:
        data = f.read().rstrip()
    if data != password:
        return generate_answer({'ok': False})



@app.route('/check_password')
def check_password():
    with open('password.txt') as f:
        password = f.read().rstrip()
    if request.args.get('password') != password:
        return generate_answer({'ok': False})
    return generate_answer({'ok': True})


@app.route('/admin')
def admin():
    if not is_authorized():
        return redirect(url_for('login'))
    devs = Device.query.all()[1:]
    return render_template('main.html', devices=devs, config=config)


@app.route('/delete-device/<int:id>')
def delete_device(id):
    if not is_authorized():
        return redirect(url_for('login'))
    dev = Device.query.filter_by(id=id).first()
    no_device = Device.query.filter_by(id=1).first()
    pin = Pin.query.filter_by(device=dev).first()
    pin.device = no_device
    db.session.add(pin)
    db.session.commit()
    db.session.delete(dev)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', success=True)
    else:
        password = request.form['password']
        with open('password.txt') as f:
            data = f.read().rstrip()
        if data == password:
            session['authed'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', success=False)


@app.route('/add-device', methods=['GET', 'POST'])
def add_device():
    if not is_authorized():
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('add-device.html', config=config)
    else:
        type = int(request.form['type'])
        pin = int(request.form['pin'])
        pinn = Pin.query.filter_by(signature=pin).first()
        if pinn.device.id != 1:
            return render_template('add-device.html', config=config, no_pin=True)
        dev = Device(type=type)
        pinn.device = dev
        db.session.add(dev)
        db.session.commit()
        db.session.add(pinn)
        db.session.commit()
        return redirect(url_for('admin'))
