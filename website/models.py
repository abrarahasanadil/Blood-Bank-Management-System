from . import db
from flask_login import UserMixin


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer, db.ForeignKey('user.gender'))
    gender = db.Column(db.String(1), db.ForeignKey('user.gender'))
    blood_type = db.Column(db.String(3), db.ForeignKey('blood.blood_type'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer, db.ForeignKey('user.gender'))
    gender = db.Column(db.String(1), db.ForeignKey('user.gender'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer, unique=True)

class Bloodbank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(100))

class Blood(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), db.ForeignKey('user.blood_type'))
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bloodbank_id = db.Column(db.Integer, db.ForeignKey('bloodbank.id'))

class Blooddelivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bloodbank_id = db.Column(db.Integer, db.ForeignKey('bloodbank.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(150), unique=True)
    blood_type = db.Column(db.String(3))
    gender = db.Column(db.String(1))
    password = db.Column(db.String(150))

