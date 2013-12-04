
from flask import render_template, url_for, request, session, g
from flask import Blueprint, current_app as app


charts = Blueprint('charts', __name__, url_prefix='/charts')


@charts.route('/')
def over_time():
    return render_template('charts/over_time.html')

@charts.route('/average/by_hour')
def avg_by_hour():
    return render_template('charts/avg_by_hour.html')
