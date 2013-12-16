
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

# The EUI returns cost as a multiple of this number
# divide any cost by this to get an accurate cost
COST_MULTIPLIER = 100000

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


@data.route('/series.<string:ext>')
@login_required
def data(ext=None):
    aggregator = request.args.get('agg')
    grouping = request.args.get('grp')
    if not aggregator or not grouping:
        app.logger.debug("invalid params")
        abort(404)
    validate_params(aggregator, grouping)

    start = request.args.get('start')
    end = request.args.get('end')
    owner_id = g.user.get_id()

    groups = ['year', 'month', 'week', 'day', 'hour']

    sql = """
    select
        min(id) as id,
        min(start) as start,
        {agg}(cost) as cost,
        {agg}(value) as value
    from data_view
    where owner = {owner_id}
    """.format(owner_id = owner_id)

    if start:
        sql += " and start >= '%s'::date " % start
    if end:
        sql += " and start < '%s'::date " % end

    sql += "\ngroup by "
    # this takes the sublist of `groups` up to the index of `grouping`
    # eg. week -> ['year', 'month', 'week']
    # eg. year -> ['year']
    sql += ', '.join(groups[:groups.index(grouping) + 1])
    sql += "\norder by id"

    app.logger.debug('executing sql \n%s' % sql)

    if ext == 'json':
        return json_serialize_query(sql, datum_factory)
    elif ext == 'csv':
        return csv_serialize_query(sql, datum_factory)
    else:
        app.logger.info("extension '%s' not supported")
        abort(404)

def datetime_string(t):
    return "%s-%s-%s" % (t.year, t.month, t.day)


@data.route('/dashboard')
@login_required
def dashboard():
    dash_data = {}
    now = datetime.datetime.now() - datetime.timedelta(days=365)
    day = datetime.timedelta(days=1)
    week = datetime.timedelta(days=7)
    today_midnight = datetime.datetime(now.year, now.month, now.day)
    yesterday_midnight = today_midnight - day

    owner_id = g.user.get_id()

    # today's usage so far
    sql_today = """
    select sum(value), sum(cost)
    from data_view
    where owner = {owner_id}
    and start >= '{start}'::date
    and start < '{end}'::date
    """.format(
        owner_id = owner_id,
        start = datetime_string(today_midnight),
        end = datetime_string(now + day)
    )
    rows = db.engine.execute(sql_today)
    today_sum_value, today_sum_cost = rows.first()

    # yesterday's usage
    sql_yesterday = """
    select sum(value), sum(cost)
    from data_view
    where owner = {owner_id}
    and start >= '{start}'::date
    and start < '{end}'::date
    """.format(
        owner_id = owner_id,
        start = datetime_string(yesterday_midnight),
        end = datetime_string(today_midnight)
    )
    rows = db.engine.execute(sql_yesterday)
    yesterday_sum_value, yesterday_sum_cost = rows.first()

    # avg daily
    sql_avg_daily = """
    -- select the average over all day's summed energy usage
    select
        avg(value) as value,
        avg(cost) as cost
    from (
        -- select the sum of each day's energy usage
        select
            min(id) as id,
            min(start) as start,
            sum(value) as value,
            sum(cost) as cost
        from data_view
        where owner = {owner_id}
        group by year, month, day
    ) as avg_by_day
    """.format(owner_id = owner_id)
    rows = db.engine.execute(sql_avg_daily)
    daily_avg_value, daily_avg_cost = rows.first()

    # last week
    sql_last_week = """
    select
        sum(cost) as cost,
        sum(value) as value
    from data_view
    where owner = {owner_id}
    and start >= '{start}'::date
    and start < '{end}'::date
    """.format(
        owner_id = owner_id,
        start = datetime_string(today_midnight - week),
        end = datetime_string(today_midnight)
    )
    rows = db.engine.execute(sql_last_week)
    last_week_cost, last_week_value = rows.first()

    # avg weekly
    sql_avg_weekly = """
    select
        avg(value) as value,
        avg(cost) as cost
    from (
        select
            min(id) as id,
            min(start) as start,
            sum(value) as value,
            sum(cost) as cost,
            div(cast(day as integer), 7) as week
        from data_view
        where owner = {owner_id}
        -- can't include week 4, half weeks
        and day < 28
        group by year, month, week
    ) as avg_by_week
    """.format(owner_id = owner_id)
    rows = db.engine.execute(sql_avg_weekly)
    weekly_avg_value, weekly_avg_cost = rows.first()


    dash_data['todaySoFar'] = float( today_sum_cost ) / COST_MULTIPLIER
    dash_data['yesterdayUsage'] = float ( yesterday_sum_value )
    dash_data['dailyAverage'] = float( daily_avg_value )
    dash_data['weeklyUsage'] = float( last_week_value )
    dash_data['weeklyAverage'] = float( weekly_avg_value )
    dash_data['sleepingUsage'] = 30
    return json.dumps(dash_data)


