
from flask import redirect, url_for, render_template, session, request, \
        abort, g
from flask import Blueprint, current_app as app
from flask import Response
from flask.ext.login import login_required

from datetime import datetime, timedelta
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


def to_date_string(t):
    # returns the "yyyy-mm-dd"
    return datetime.strftime(t, "%Y-%m-%d")

def from_date_string(s):
    # using my standard "yyyy-mm-dd"
    return datetime.strptime(s, "%Y-%m-%d")

def json_serialize_query(sql, datum_factory):
    queryset = db.engine.execute(sql)
    results = []
    row = None # allocate row at this scope so I can see it in the except
    try:
        for row in queryset:
            datum = datum_factory(row)
            results.append(dict(datum))
    except TypeError as e:
        app.logger.debug("caught typeerror: assuming no results.\n\
        offensive row is %s\nexception is: %s" % (row, e))
        pass
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
    app.logger.debug('executing sql\n%s' % sql)
    res = db.engine.execute(sql)
    date = res.first()
    if date:
        return json.dumps(date[0], default=date_handler)
    else:
        return '0'


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
        abort(400)
    if grouping not in GROUPS:
        app.logger.debug("can't group by %s" % grouping)
        abort(400)

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
        abort(400)


@data.route('/goals', methods=['GET'])
@login_required
def goals():
    owner_id = g.user.get_id()
    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)

    goals = []

    goals_sql = """
    select * from goals
    where goals.user = {owner_id}
    """.format(owner_id = owner_id)

    goals_rows = db.engine.execute(goals_sql)

    for goal_row in goals_rows:
        id, user, target, scope = goal_row
        goal = {}
        goal['id'] = id
        goal['target'] = target
        goal['scope'] = scope

        if scope == 'week':
            # exclude month from this grouping, or else weeks get chopped
            grouping = 'year, week'
        else:
            # this takes the sublist of `groups` up to the index of `scope`
            # eg. week -> ['year', 'month', 'week']
            # eg. year -> ['year']
            grouping = ', '.join(GROUPS[:GROUPS.index(scope) + 1])

        result_sql = """
        select
        max(start) as start,
        date_part('year', max(start)) as year,
        date_part('month', max(start)) as month,
        date_part('week', max(start)) as week,
        date_part('day', max(start)) as day,
        date_part('hour', max(start)) as hour,
        sum(cost) as cost,
        sum(value) as value,
        date_part('days',
          date_trunc('month', max( start ))
            + '1 month'::interval
            - date_trunc('month', max( start ))
          ) as days_in_month,
        extract(dow from max(start)) as day_of_week
        from data_view
        where owner = {owner_id}
        group by {grouping}
        order by start desc
        limit 1
        """.format(owner_id = owner_id, grouping = grouping)

        app.logger.debug('executing result_sql:\n%s' % result_sql)
        row = db.engine.execute(result_sql).first()
        # unpack values in row
        start, year, month, week, day, hour, cost, value, dmonth, dweek = row

        goal['start'] = 1
        goal['value'] = float(value)
        goal['cost'] = float(cost)

        if scope == 'week':
            goal['end'] = 7                 # num days in week
            goal['current'] = int(dweek)    # current day of the week
        elif scope == 'month':
            goal['end'] = int(dmonth)       # num days in month
            goal['current'] = float(day)    # current day of month
        else: # scope is daily
            goal['current'] = 0

        goal['current'] += hour/24.0 # amount of the day that has passed

        goals.append(goal)

    sql = """
    select
        'week' as scope,
        avg(week_q.cost) as cost,
        avg(week_q.value) as value
    from (
        select
            sum(cost) as cost,
            sum(value) as value
        from data_view
        where owner = {owner_id}
        group by week
    ) as week_q

    union

    select
        'month' as scope,
        avg(monthq.cost) as cost,
        avg(monthq.value) as value
    from (
        select
            sum(cost) as cost,
            sum(value) as value
        from data_view
        where owner = {owner_id}
        group by month
    ) as monthq
    order by scope
    """.format(owner_id = owner_id)

    app.logger.debug('executing sql for goal avgs:\n%s' % sql)
    res = db.engine.execute(sql)

    month, week = [{
        'scope': x[0],
        'cost': float(x[1]),
        'value': float(x[2])
        } for x in res]

    app.logger.debug('month: %s\nweek: %s' % (month, week))

    result = {}
    result['goals'] = goals
    result['averages'] = [month, week]
    return json.dumps(result, indent=4)


@data.route('/goals', methods=['POST'])
@data.route('/goals/<int:goal_id>', methods=['POST'])
@login_required
def save_goal(goal_id=None):
    app.logger.debug('save goal with goal id: %s' % goal_id)
    if goal_id:
        goal = schema.Goal.query.get(int(goal_id))
        app.logger.debug('got goal', goal)
    else:
        goal = schema.Goal()
    goal.user = g.user.get_id()
    goal.target = request.args.get('target')
    goal.scope = request.args.get('scope')
    db.session.add(goal)
    app.logger.debug("committing: %s" % db.session.dirty)
    db.session.commit()
    return "success"


@data.route('/goals/<int:goal_id>/delete', methods=["POST"])
@login_required
def delete_goal(goal_id):
    app.logger.debug('delete goal with goal id: %s' % goal_id)

    goal = schema.Goal.query.get(int(goal_id))
    app.logger.debug('about to delete goal: %s' % goal)
    db.session.delete(goal)
    db.session.commit()
    return 'success'


@data.route('/today')
@login_required
def today():
    owner_id = g.user.get_id()
    series = request.args.get('series')
    date = request.args.get('date')

    if not date:
        app.logger.debug("no parameter 'date' provided, 400")
        abort(400)

    this_date = from_date_string(date)
    one_day = timedelta(days=1)

    if series:
        sql = """
        select
            start,
            'value' as type,
            cost,
            value
        from (
            select start, cost, value
            from data_view
            where owner = {owner_id}
            and start >= '{date}'::date
            order by start desc
            limit 24
        ) as q

        union

        select
            min(start) as start,
            'aggregate' as type,
            avg(cost) as cost,
            avg(value) as value
        from data_view
        where owner = {owner_id}
        group by hour

        order by type, start
        """.format(
            owner_id = owner_id,
            date = to_date_string(this_date - one_day)
        )

    else:
        sql = """
        -- select sum over things happening today
        select
            min(start) as start,
            'value' as type,
            sum(cost) as cost,
            sum(value) as value
        from data_view
        where owner = {owner_id}
        and start >= '{start_date}'::date
        and start < '{end_date}'::date
        """.format(
            owner_id = owner_id,
            start_date = to_date_string(this_date),
            end_date = to_date_string(this_date + one_day)
        )

    def datum_factory(row):
        return {
            'start': str(row[0]),
            'type': str(row[1]),
            'cost': float(row[2]),
            'value': float(row[3])
        }

    return json_serialize_query(sql, datum_factory)


@data.route('/yesterday')
@login_required
def yesterday():
    owner_id = g.user.get_id()
    date = request.args.get('date')
    series = request.args.get('series')

    if not date:
        app.logger.debug("no parameter 'date' provided, 400")
        abort(400)

    this_date = from_date_string(date)
    one_day = timedelta(days=1)

    if series:
        sql = """
        select
            min(start) as start,
            'value' as type,
            sum(cost) as cost,
            sum(value) as value
        from data_view
        where owner = {owner_id}
        group by year, month, day

        UNION

        select
            min(start) as start,
            'aggregate' as type,
            avg(cost) as cost,
            avg(value) as value
        from (
            select
                min(start) as start,
                sum(cost) as cost,
                sum(value) as value
            from data_view
            where owner = {owner_id}
            group by year, month, day
        ) as query
        """.format( owner_id = owner_id )

    else:
        sql = """
        -- select sum over things happening yesterday
        select
            min(start) as start,
            'value' as type,
            sum(cost) as cost,
            sum(value) as value
        from data_view
        where owner = {owner_id}
        and start >= '{start_date}'::date
        and start < '{end_date}'::date

        UNION
        -- select daily average
        select
            min(start) as start,
            'aggregate' as type,
            avg(cost) as cost,
            avg(value) as value
        from (
            select
                min(start) as start,
                sum(cost) as cost,
                sum(value) as value
            from data_view
            where owner = {owner_id}
            group by year, month, day
        ) as query
        """.format(
            owner_id = owner_id,
            start_date = to_date_string(this_date - one_day),
            end_date = to_date_string(this_date)
        )

    def datum_factory(row):
        return {
            'start': str(row[0]),
            'type': str(row[1]),
            'cost': float(row[2]),
            'value': float(row[3])
        }

    return json_serialize_query(sql, datum_factory)


@data.route('/week')
@login_required
def week():
    owner_id = g.user.get_id()
    date = request.args.get('date')
    series = request.args.get('series')

    if not date:
        app.logger.debug("no parameter 'date' provided, 400")
        abort(400)

    this_date = from_date_string(date)
    one_week = timedelta(days=7)

    if series:
        sql = """
        select
            min(start) as start,
            'value' as type,
            sum(cost) as cost,
            sum(value) as value
        from data_view
        where owner = {owner_id}
        group by year, week

        UNION

        select
            min(start) as start,
            'aggregate' as type,
            avg(cost) as cost,
            avg(value) as value
        from (
            select min(start) as start,
            sum(cost) as cost,
            sum(value) as value
            from data_view
            where owner = {owner_id}
            group by year, week
        ) as query
        """.format( owner_id = owner_id )

    else:
        sql = """
        select
            min(start) as start,
            'value' as type,
            sum(cost) as cost,
            sum(value) as value
        from data_view
        where owner = {owner_id}
        and start >= '{start_date}'::date
        and start < '{end_date}'::date

        UNION

        select
            min(start) as start,
            'aggregate' as type,
            avg(cost) as cost,
            avg(value) as value
        from (
            select
                min(start) as start,
                sum(cost) as cost,
                sum(value) as value
            from data_view
            where owner = {owner_id}
            group by year, week
        ) as query
        """.format(
            owner_id = owner_id,
            start_date = to_date_string(this_date - one_week),
            end_date = to_date_string(this_date)
        )

    def datum_factory(row):
        return {
            'start': str(row[0]),
            'type': str(row[1]),
            'cost': float(row[2]),
            'value': float(row[3])
        }

    return json_serialize_query(sql, datum_factory)



