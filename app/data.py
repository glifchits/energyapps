
from flask import redirect, url_for, render_template, session, request, \
        abort, g
from flask import Blueprint, current_app as app
from flask.ext.login import login_required

import datetime
import json

import schema


data = Blueprint('data', __name__, url_prefix='/data')


@data.route('/readings')
@login_required
def get_readings(id=None):
    start = request.args.get('start')
    end = request.args.get('end')

    readings = schema.Reading.query.all()
    app.logger.debug('readings: %s ' % readings)

    my_json = [{
            'id': reading.id,
            'title': reading.title
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


