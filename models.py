from app import db


class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))


class Pin(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    signature = db.Column(db.Integer)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('pins', lazy=True))


# db.create_all()
# dev = Device(type=0)
# db.session.add(dev)
# db.session.commit()
# dev = Device.query.filter_by(type=0).first()
# for i in range(1, 14):
#     pin = Pin(signature=i, device=dev)
#     db.session.add(pin)
#     db.session.commit()
