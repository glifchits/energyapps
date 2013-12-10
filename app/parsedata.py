
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
import xml.etree.ElementTree as ET
import datetime

import schema

#from __init__ import db

class DecoyDB:
    class Session:
        def __getattr__(self, key):
            pass
        def add(*args):
            pass
        def commit(*args):
            pass
    session = Session()
db = DecoyDB()

import config

ENTRY = '{http://www.w3.org/2005/Atom}entry'
CONTENT = '{http://www.w3.org/2005/Atom}content'

USAGE_POINT = '{http://naesb.org/espi}UsagePoint'
SERVICE_CATEGORY = '{http://naesb.org/espi}ServiceCategory'
KIND = '{http://naesb.org/espi}kind'
LOCAL_TIME = '{http://naesb.org/espi}LocalTimeParameters'
METER_READING = '{http://naesb.org/espi}MeterReading'
INTERVAL_BLOCK = '{http://naesb.org/espi}IntervalBlock'
READING_TYPE = '{http://naesb.org/espi}ReadingType'
TITLE = '{http://www.w3.org/2005/Atom}title'

def from_timestamp(timestamp):
    if type(timestamp) == str:
        timestamp = int(timestamp)
    return datetime.datetime.fromtimestamp(timestamp)


def process_data(xml_string):
    root = ET.fromstring(xml_string)

    kind = root.findall(ENTRY)[0] \
            .find(CONTENT) \
            .find(USAGE_POINT) \
            .find(SERVICE_CATEGORY) \
            .find(KIND)

    dst_end, dst_offset, dst_start, tz_offset = root.findall(ENTRY)[1]\
            .find(CONTENT) \
            .find(LOCAL_TIME) \
            .getchildren()

    data_type = root.findall(ENTRY)[2].find(TITLE).text

    interval_blocks = root.findall(ENTRY)[3] \
            .find(CONTENT) \
            .findall(INTERVAL_BLOCK)

    reading_type = root.findall(ENTRY)[4] \
            .find(CONTENT) \
            .find(READING_TYPE)

    print data_type

    accumulation_behaviour, commodity, currency, data_qualifier, flow_direction, \
    interval_length, kind, phase, multiplier, time_attribute, uom \
        = reading_type.getchildren()

    reading = schema.Reading(
        title = "mydata",
        accumulation_behaviour = accumulation_behaviour.text,
        commodity = commodity.text,
        currency = currency.text,
        data_qualifier = data_qualifier.text,
        flow_direction = flow_direction.text,
        interval_length = interval_length.text,
        kind = kind.text,
        multiplier = multiplier.text,
        uom = uom.text,
        service_kind = kind.text
    )

    try:
        user = g.user
        if user:
            user.readings.append(reading)
    except NameError:
        pass

    db.session.add(reading)

    for block in interval_blocks:
        children = block.getchildren()
        interval_readings = children[1:]

        for i_reading in interval_readings:
            cost, time_period, value = i_reading.getchildren()
            duration, start = time_period.getchildren()

            interval_reading = schema.Interval(
                start = from_timestamp(start.text),
                duration = duration.text,
                cost = cost.text,
                value = value.text
            )
            reading.intervals.append(interval_reading)

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

