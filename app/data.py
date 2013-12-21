
from flask import redirect, url_for, render_template, session, request, \
        abort, g
from flask import Blueprint, current_app as app
from flask import Response
from flask.ext.login import login_required

import datetime
import json
import csv
import cStringIO

import schema
db = schema.db

data = Blueprint('data', __name__, url_prefix='/data')

# The EUI returns cost as a multiple of this number
# divide any cost by this to get an accurate cost
COST_MULTIPLIER = 100000
AGGREGATORS = ['avg', 'sum', 'min', 'max']
GROUPS = ['year', 'month', 'week', 'day', 'hour']


def datetime_string(t):
    return "%s-%s-%s" % (t.year, t.month, t.day)

def json_serialize_query(sql, datum_factory):
    queryset = db.engine.execute(sql)
    results = []
    for row in queryset:
        datum = datum_factory(row)
        results.append(dict(datum))
    res = json.dumps(results, indent=4)
    response = Response(res, status=200, mimetype='application/json')
    return response

def csv_serialize_query(sql, datum_factory):
    queryset = db.engine.execute(sql)
    out = cStringIO.StringIO()
    writer = csv.writer(out)
    headers = False
    for row in queryset:
        datum = datum_factory(row)
        if not headers:
            writer.writerow(datum.keys())
            headers = True
        writer.writerow(datum.values())

    val = out.getvalue()
    out.close()
    response = Response(val, status=200, mimetype='text/csv')
    return response

def date_handler(obj):
    # `http://blog.codevariety.com/2012/01/06/python-serializing-dates-datetime-datetime-into-json/`
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

@data.route('/last_date')
@login_required
def last_data_date():
    owner_id = g.user.get_id()
    sql = """
    select start from data_view
    where owner = {owner_id}
    order by start desc
    limit 1
    """.format(owner_id = owner_id)
    res = db.engine.execute(sql)
    return json.dumps(res.first()[0], default=date_handler)


@data.route('/series.<string:ext>')
@login_required
def series(ext=None):
    owner_id = g.user.get_id()
    if not owner_id:
        app.logger.debug("couldn't get user id, not logged in I guess")
        abort(401)

    aggregator = request.args.get('agg') or 'sum'
    grouping = request.args.get('grp') or 'hour'
    if aggregator not in AGGREGATORS:
        app.logger.debug("can't aggregate by %s" % aggregator)
        abort(404)
    if grouping not in GROUPS:
        app.logger.debug("can't group by %s" % grouping)
        abort(404)

    agg2 = request.args.get('agg2')
    last = request.args.get('last') or 'false'
    start = request.args.get('start')
    end = request.args.get('end')

    sql = ''
    if agg2:
        sql += """
    select
        min(id) as id,
        min(start) as start,
        {agg}(cost) as cost,
        {agg}(value) as value
    from (""".format(agg = agg2)
    sql += """
    select
        min(id) as id,
        min(start) as start,
        {agg}(cost) as cost,
        {agg}(value) as value
    from data_view
    where owner = {owner_id}
    """.format(owner_id = owner_id, agg = aggregator)
    if start:
        sql += " and start >= '%s'::date " % start
    if end:
        sql += " and start < '%s'::date " % end
    sql += "\ngroup by "
    # this takes the sublist of `groups` up to the index of `grouping`
    # eg. week -> ['year', 'month', 'week']
    # eg. year -> ['year']
    sql += ', '.join(GROUPS[:GROUPS.index(grouping) + 1])
    sql += "\norder by id"
    if last == 'true' and not agg2:
        sql += " desc\nlimit 1"
    if agg2:
        sql += "\n) as sub_query"

    app.logger.debug('executing sql \n%s' % sql)

    def datum_factory(row):
        return {
            "id": int(row[0]),
            "start": str(row[1]),
            "cost": float(row[2]),
            "value": float(row[3])
        }

    if ext == 'json':
        return json_serialize_query(sql, datum_factory)
    elif ext == 'csv':
        return csv_serialize_query(sql, datum_factory)
    else:
        app.logger.info("extension '%s' not supported")
        abort(404)

