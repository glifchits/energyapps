try:
#    from flask import g
#    from flask import current_app as app
    assert True == False
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

class DecoyDB:
    class Session:
        def __getattr__(self, key): pass
        def add(*args): pass
        def commit(*args): pass
    session = Session()
db = DecoyDB()

#from __init__ import db

def from_timestamp(timestamp):
    if type(timestamp) == str:
        timestamp = int(timestamp)
    return datetime.datetime.fromtimestamp(timestamp)


def process_data(xml_string):
    data = GreenButtonData(xml_string).form_tree()

    eui = schema.EnergyUsageInformation()
    eui.title = data.title
    eui.service_kind = data.service_kind
    eui.dst_start_rule = data.local_time.dst_start_rule
    eui.dst_end_rule = data.local_time.dst_end_rule
    eui.dst_offset = data.local_time.dst_offset
    eui.tz_offset = data.local_time.tz_offset

    try:
        user = g.user
        user.eui.append(eui)
    except NameError:
        db.session.add(eui)

    for meter_reading in data.meter_readings:
        interval_block = meter_reading.interval_block
        reading_type = meter_reading.reading_type

        reading = schema.MeterReading()
        reading.accumulation_behaviour = reading_type.accumulation_behaviour
        reading.commodity = reading_type.commodity
        reading.currency = reading_type.currency
        reading.data_qualifier = reading_type.data_qualifier
        reading.flow_direction = reading_type.flow_direction
        reading.interval_length = reading_type.interval_length
        reading.kind = reading_type.kind
        reading.multiplier = reading_type.multiplier
        reading.uom = reading_type.uom

        for interval_reading in interval_block.interval_readings:
            interval = schema.Interval()
            interval.start = interval_reading.start
            interval.duration = interval_reading.duration
            interval.cost = interval_reading.cost
            interval.value = interval_reading.value
            reading.intervals.append(interval)


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

