
from flask import redirect, url_for, render_template, session, request, \
        abort, g
from flask import Blueprint, current_app as app
from flask.ext.login import login_required

import datetime
import json
import csv
import cStringIO

import schema
db = schema.db


data = Blueprint('data', __name__, url_prefix='/data')


def json_serialize_query(sql, datum_factory):
    queryset = db.engine.execute(sql)
    results = []
    for row in queryset:
        datum = datum_factory(row)
        results.append(dict(datum))
    return json.dumps(results, indent=4)

def csv_serialize_query(sql, datum_factory):
    queryset = db.engine.execute(sql)

    out = cStringIO.StringIO()
    writer = csv.writer(out)

    headers = False
    for row in queryset:
        datum = datum_factory(row)
        if not headers:
            writer.writerow([val[0] for val in datum])
            headers = True
        writer.writerow([val[1] for val in datum])

    val = out.getvalue()
    out.close()
    return val


def validate_params(aggregator, grouping):
    if aggregator not in ['avg', 'sum', 'min', 'max']:
        app.logger.debug('can\'t aggregate by %s' % aggregator)
        abort(404)
    if grouping not in ['hour', 'day', 'month', 'year']:
        app.logger.debug('can\'t group by %s' % grouping)
        abort(404)


@data.route('/all')
@data.route('/all.<string:ext>')
@login_required
def all(ext=None):
    app.logger.debug("/all route with extension %s" % ext)
    start = request.args.get('start')
    end = request.args.get('end')

    owner_id = g.user.get_id()

    sql = """select id, start, cost, value from data_view
    where owner = {owner_id}""".format(owner_id = owner_id)
    if start:
        sql += " and start >= '%s'::date " % start
    if end:
        sql += " and start < '%s'::date " % end
    sql += "\norder by id"

    def datum_fac(row):
        return (
            ('id', row[0]),
            ('start', str(row[1])),
            ('cost', round(row[2], 2)),
            ('value', round(row[3], 2))
        )

    if not ext or ext == 'json':
        return json_serialize_query(sql, datum_fac)
    elif ext == 'csv':
        return csv_serialize_query(sql, datum_fac)
    else:
        app.logger.info("extension '%s' not supported")
        abort(404)


@data.route('/group')
@data.route('/group.<string:ext>')
@login_required
def group(ext=None):
    aggregator = request.args.get('agg')
    grouping = request.args.get('grp')

    # defaults for chart render
    if not ext:
        aggregator = aggregator or 'sum'
        grouping = grouping or 'month'

    if not aggregator or not grouping:
        app.logger.debug("invalid params")
        abort(404)
    validate_params(aggregator, grouping)

    start = request.args.get('start')
    end = request.args.get('end')

    owner_id = g.user.get_id()

    sql = '''
    select min(id) as minid,
        min(start) as minstart,
        {aggregator}(cost) as cost,
        {aggregator}(value) as value,
        {grouping}
    from data_view
    where owner = {owner_id}
    '''
    if start:
        sql += " and start >= '%s'::date " % start
    if end:
        sql += " and start < '%s'::date " % end
    sql += "\ngroup by {grouping}\norder by minid"

    sql = sql.format( aggregator = aggregator, grouping = grouping,
            owner_id = owner_id)
    app.logger.debug('executing sql\n%s' % sql)

    def datum_factory(row):
        return (
            ('id', row[0]),
            ('cost', round(row[2], 2)),
            ('value', round(row[3], 2)),
            (grouping, int(row[4]))
        )

    if not ext:
        return render_template('charts/grouped.html')
    elif ext == 'json':
        return json_serialize_query(sql, datum_factory)
    elif ext == 'csv':
        return csv_serialize_query(sql, datum_factory)
    else:
        app.logger.info("extension '%s' not supported")
        abort(404)


@data.route('/aggregate')
@data.route('/aggregate.<string:ext>')
def aggregate(ext=None):
    aggregator = request.args.get('agg')
    grouping = request.args.get('grp')
    if not aggregator or not grouping:
        app.logger.debug("invalid params")
        abort(404)
    validate_params(aggregator, grouping)

    start = request.args.get('start')
    end = request.args.get('end')

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
    sql += "from interval "

    if start or end:
        sql += "\nwhere "
    if start:
        sql += " start >= '%s'::date " % start
    if start and end:
        sql += " and "
    if end:
        sql += " start < '%s'::date " % end

    sql += "\ngroup by "
    sql += ', '.join(groups[:groups.index(grouping) + 1])
    sql += "\norder by minid"

    def datum_factory(row):
        d = [
            ('id', row[0]),
            ('cost', round(row[1], 2)),
            ('value', round(row[2], 2)),
            ('year', int(row[3]))
        ]
        if lte(grouping, 'month'):
            d.append( ('month', int(row[4])) )
        if lte(grouping, 'day'):
            d.append( ('day', int(row[5])) )
        if lte(grouping, 'hour'):
            d.append( ('hour', int(row[6])) )
        return d

    app.logger.debug('executing sql \n%s' % sql)

    if not ext:
        return render_template('charts/aggregate.html')
    elif ext == 'json':
        return json_serialize_query(sql, datum_factory)
    elif ext == 'csv':
        return csv_serialize_query(sql, datum_factory)
    else:
        app.logger.info("extension '%s' not supported")
        abort(404)
