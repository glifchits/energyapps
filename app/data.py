
from flask import redirect, url_for, render_template, session, request, \
        abort, g
from flask import Blueprint, current_app as app
from flask.ext.login import login_required

import datetime
import json

import schema


data = Blueprint('data', __name__, url_prefix='/data')


def interval_readings(reading_id=None):
    """Gets the <IntervalReading> objects for this user.
    If `reading_id` is specified, gets from <Reading `id`>, otherwise
    gets from the first <Reading>.
    """
    u_readings = g.user.readings
    if not reading_id:
        reading = u_readings.first()
    else:
        reading = u_readings.filter(schema.Reading.id == reading_id).first()
    intervals = reading.intervals.all()
    readings = [i.readings.all() for i in intervals]
    readings = reduce(lambda x, y: x + y, readings)
    return readings


@data.route('/readings')
@data.route('/readings/<id>')
@login_required
def get_readings(id=None):
    start = request.args.get('start')
    end = request.args.get('end')

    readings = interval_readings(id)

    my_json = [{
            'start': str(reading.start),
            'duration': reading.duration,
            'cost': reading.cost,
            'value': reading.value
        } for reading in readings]
    return json.dumps(my_json, indent=4)


@data.route('/hour')
@data.route('/hour/<id>')
@login_required
def by_hour(id=None):
    readings = interval_readings(id)

    data = dict([(h,[]) for h in range(0, 24)])

    for reading in readings:
        hour = reading.start.hour
        data[hour].append(reading)

    for hour in data.keys():
        data[hour] = [{
                'start' : str(reading.start),
                'cost' : reading.cost,
                'value' : reading.value
            } for reading in data[hour]]

    return json.dumps(data, indent=4)


