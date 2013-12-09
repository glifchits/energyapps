
from flask import redirect, url_for, render_template, session, request, \
        abort, g
from flask import Blueprint, current_app as app
from flask.ext.login import login_required

import datetime
import json

import schema
db = schema.db


data = Blueprint('data', __name__, url_prefix='/data')


def serialize_query(sql, datum_factory):
    queryset = db.engine.execute(sql)
    results = []
    for row in queryset:
        datum = datum_factory(row)
        results.append(datum)
    return json.dumps(results, indent=4)


@data.route('/')
def all():
    sql = '''
    select id, start, cost, value from interval;
    '''
    def datum_fac(row):
        return { 'id': row[0],
            'start': str(row[1]),
            'cost': row[2],
            'value': row[3] }
    return serialize_query(sql, datum_fac)


@data.route('/group/<string:aggregator>/<string:grouping>')
def group(aggregator, grouping):
    if aggregator not in ['avg', 'sum', 'min']:
        app.logger.debug('can\'t aggregate by %s' % aggregator)
        abort(404)
    if grouping not in ['hour', 'day', 'month', 'year']:
        app.logger.debug('can\'t group by %s' % grouping)
        abort(404)

    sql = '''
    select min(id) as minid,
        min(start) as minstart,
        {aggregator}(cost) as cost,
        {aggregator}(value) as value,
        date_part('{grouping}', start) as {grouping}
    from interval
    group by {grouping}
    '''.format( aggregator = aggregator, grouping = grouping )
    app.logger.debug('executing sql\n%s' % sql)

    def datum_factory(row):
        return {
            'id': row[0],
            'cost': row[2],
            'value': row[3],
            grouping: row[4] }
    return serialize_query(sql, datum_factory)


