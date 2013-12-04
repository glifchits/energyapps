
from flask import redirect, url_for, render_template, session, request, \
        abort, g
from flask import Blueprint, current_app as app
from flask.ext.login import login_required

import datetime
import json

import schema


data = Blueprint('data', __name__, url_prefix='/data')


@data.route('/readings')
@data.route('/readings/<id>')
@login_required
def get_readings(id=None):
    start = request.args.get('start')
    end = request.args.get('end')

    if id == None:
        reading = g.user.readings.first()
    else:
        reading = g.user.readings.filter(schema.Reading.id == id).first()
    intervals = reading.intervals.all()

    readings = [i.readings.all() for i in intervals]
    readings = reduce(lambda x, y: x + y, readings)

    my_json = [{
            'start': str(reading.start),
            'duration': reading.duration,
            'cost': reading.cost,
            'value': reading.value
        } for reading in readings]
    return json.dumps(my_json, indent=4)


