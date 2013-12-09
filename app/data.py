
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


def validate_params(aggregator, grouping):
    if aggregator not in ['avg', 'sum', 'min', 'max']:
        app.logger.debug('can\'t aggregate by %s' % aggregator)
        abort(404)
    if grouping not in ['hour', 'day', 'month', 'year']:
        app.logger.debug('can\'t group by %s' % grouping)
        abort(404)


@data.route('/')
def all():
    sql = '''
    select id, start, cost, value from interval;
    '''
    def datum_fac(row):
        return { 'id': row[0],
            'start': str(row[1]),
            'cost': round(row[2], 2),
            'value': round(row[3], 2) }
    return serialize_query(sql, datum_fac)


@data.route('/group/<string:aggregator>/<string:grouping>')
def group(aggregator, grouping):
    validate_params(aggregator, grouping)
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
            'cost': round(row[2], 2),
            'value': round(row[3], 2),
            grouping: row[4] }
    return serialize_query(sql, datum_factory)


@data.route('/aggregate/<string:aggregator>/<string:grouping>')
def aggregate(aggregator, grouping='hour'):
    validate_params(aggregator, grouping)

    groups = ['year', 'month', 'day', 'hour']
    def lte(g1, g2):
        i1 = groups.index(g1)
        i2 = groups.index(g2)
        return i1 >= i2

    sql = '''
    select min(id) as minid,
        {aggregator}(cost) as cost,
        {aggregator}(value) as value,
        date_part('year', start) as year
    '''.format(aggregator = aggregator)
    if lte(grouping, 'month'):
        sql += ", date_part('month', start) as month\n"
    if lte(grouping, 'day'):
        sql += ", date_part('day', start) as day\n"
    if lte(grouping, 'hour'):
        sql += ", date_part('hour', start) as hour\n"

    sql += "from interval\ngroup by "
    sql += ', '.join(groups[:groups.index(grouping) + 1])

    def datum_factory(row):
        d = [
            ['id', row[0]],
            ['cost', round(row[1], 2)],
            ['value', round(row[2])],
            ['year', int(row[3])]
        ]
        if lte(grouping, 'month'):
            d.append( ['month', int(row[4])] )
        if lte(grouping, 'day'):
            d.append( ['day', int(row[5])] )
        if lte(grouping, 'hour'):
            d.append( ['hour', int(row[6])] )
        return dict(d)

    app.logger.debug('executing sql \n%s' % sql)

    return serialize_query(sql, datum_factory)
