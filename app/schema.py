
from flask import Blueprint, current_app
from flask.ext.sqlalchemy import SQLAlchemy

import datetime

from __init__ import db


class EnergyUsageInformation(db.Model):
    __tablename__ = 'eui'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # user owning EUI
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    # from ServiceCategory
    service_kind = db.Column(db.Integer)
    # timezone info
    dst_start_rule = db.Column(db.String)
    dst_end_rule = db.Column(db.String)
    dst_offset = db.Column(db.Integer)
    tz_offset = db.Column(db.Integer)
    # readings, many children (corresponds with MeterReadings)
    meter_readings = db.relationship("MeterReading", backref='eui_readings',
            lazy='dynamic')


class MeterReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # eui owning this meter reading
    eui = db.Column(db.Integer, db.ForeignKey('eui.id'))
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
    # children (many)
    intervals = db.relationship("Interval", backref='reading_intervals',
            lazy='dynamic')

    def __repr__(self):
        return "<MeterReading %s>" % self.id


class Interval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reading_id = db.Column(db.Integer, db.ForeignKey('meter_reading.id'))
    start = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    value = db.Column(db.Integer)

    def __repr__(self):
        delta = datetime.timedelta(seconds = int(self.duration))
        return "<Interval %s-%s>" % (self.start, self.start + delta)


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    # user owning this goal
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    # attributes
    target = db.Column(db.Float)
    name = db.Column(db.String)
    scope = db.Column(db.String)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    token_retrieved = db.Column(db.DateTime)
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)
    eui_agreed = db.Column(db.Boolean)
    # children (many)
    eui = db.relationship("EnergyUsageInformation", backref='user_eui',
            lazy='dynamic')

    def __repr__(self):
        return "<User %s>" % self.name

    def set_password(self, pw):
        self.password = pw

    def check_password(self, pw):
        return self.password == pw

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def update_access_token(self, token):
        self.access_token = token
        self.token_retrieved = datetime.datetime.now()

    def agreed_to_eui(self):
        return self.eui_agreed

    def has_eui(self):
        return self.eui.count() > 0

