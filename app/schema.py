
from flask import Blueprint, current_app
from flask.ext.sqlalchemy import SQLAlchemy

from __init__ import db


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String)
    # from ReadingType
    accumulation_behaviour = db.Column(db.Integer)
    commodity = db.Column(db.Integer)
    currency = db.Column(db.Integer)
    data_qualifier = db.Column(db.Integer)
    flow_direction = db.Column(db.Integer)
    interval_length = db.Column(db.Integer)
    kind = db.Column(db.Integer)
    multiplier = db.Column(db.Integer)
    uom = db.Column(db.Integer)
    # from ServiceCategory
    service_kind = db.Column(db.Integer)

    # children (many)
    intervals = db.relationship("Interval", backref='intervals',
            lazy='dynamic')


class Interval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    reading_id = db.Column(db.Integer, db.ForeignKey('reading.id'))

    # children (many)
    readings = db.relationship("IntervalReading",
        backref='interval_readings', lazy='dynamic')


class IntervalReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interval_id = db.Column(db.Integer, db.ForeignKey('interval.id'))
    start = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    value = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def set_password(self, pw):
        self.password = pw

    def check_password(self, pw):
        return self.password == pw

    # children (many)
    readings = db.relationship("Reading",
        backref='user_readings', lazy='dynamic')
