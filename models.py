from app import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))


class SmartHome(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    webhook_url = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('smarthomes', lazy=True))


class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    type = db.Column(db.Integer)
    smarthome_id = db.Column(db.ForeignKey('smart_home.id'))
    smarthome = db.relationship('SmartHome', backref=db.backref('devices', lazy=True))


db.create_all()
