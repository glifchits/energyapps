--drop view if exists data_view; create view data_view as
select
  min(interval.id) as id,
  min(eui.owner) as owner,
  interval.start,
  round(avg(interval.duration)) as duration,
  round(avg(interval.cost) / 100000, 5) as cost,
  round(avg(interval.value), 1) as value,
  date_part('year', start) as year,
  date_part('month', start) as month,
  date_part('week', start) as week,
  date_part('day', start) as day,
  date_part('hour', start) as hour
from interval
inner join meter_reading
  on meter_reading.id = interval.reading_id
inner join eui
  on eui.id = meter_reading.eui
where meter_reading.kind = 12
group by owner, start
order by owner, start
