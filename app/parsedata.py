try:
    from flask import g
    from flask import current_app as app
except:
    import logging
    class DecoyApp:
        class Logger:
            logger = logging.Logger("parse data")
            def debug(self, msg):
                self.logger.debug(msg)
            def info(self, msg):
                self.logger.info(msg)
        logger = Logger()
    app = DecoyApp()

import sys
import os
import datetime

import schema
import config
from eui_object import GreenButtonData
'''
class DecoyDB:
    class Session:
        def __getattr__(self, key): pass
        def add(*args): pass
        def commit(*args): pass
    session = Session()
db = DecoyDB()
'''
from __init__ import db

def from_timestamp(timestamp):
    if type(timestamp) == str:
        timestamp = int(timestamp)
    return datetime.datetime.utcfromtimestamp(timestamp)


def construct_eui(data):
    eui = schema.EnergyUsageInformation(
        title = data.title,
        service_kind = data.service_kind
    )
    if data.local_time:
        eui.dst_start_rule = data.local_time.dst_start_rule
        eui.dst_end_rule = data.local_time.dst_end_rule
        eui.dst_offset = data.local_time.dst_offset
        eui.tz_offset = data.local_time.tz_offset
    return eui

def construct_meter_reading(reading_type):
    reading = schema.MeterReading(
        accumulation_behaviour = reading_type.accumulation_behaviour,
        commodity = reading_type.commodity,
        currency = reading_type.currency,
        data_qualifier = reading_type.data_qualifier,
        flow_direction = reading_type.flow_direction,
        interval_length = reading_type.interval_length,
        kind = reading_type.kind,
        multiplier = reading_type.multiplier,
        uom = reading_type.uom
    )
    return reading

def construct_interval_reading(interval_reading):
    interval = schema.Interval(
        start = from_timestamp(interval_reading.start),
        duration = interval_reading.duration,
        cost = interval_reading.cost,
        value = interval_reading.value
    )
    return interval


def process_data(xml_string):
    data = GreenButtonData(xml_string).form_tree()

    eui = construct_eui(data)

    try:
        user = g.user
        user.eui.append(eui)
    except NameError:
        db.session.add(eui)

    for meter_reading in data.meter_readings:
        interval_block = meter_reading.interval_block
        reading_type = meter_reading.reading_type

        reading = construct_meter_reading(reading_type)
        eui.meter_readings.append(reading)

        db.session.add(reading)

        for interval_reading in interval_block.interval_readings:
            interval = construct_interval_reading(interval_reading)
            reading.intervals.append(interval)
            db.session.add(interval)


    app.logger.debug('committing.\ndirty: %s\nnew: %s' % \
            (db.session.dirty, db.session.new))
    db.session.commit()
    return True



if __name__ == '__main__':
    fname = sys.argv[1]
    if not os.path.isfile(fname):
        print '%s is not a file' % fname
        sys.exit(1)
    f = open(fname, 'r')
    contents = f.read()
    process_data(contents)
    f.close()

