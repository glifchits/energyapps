create view data_view
as
select
  min(interval.id) as id,
  min(eui.owner) as owner,
  interval.start,
  avg(interval.cost) as cost,
  avg(interval.value) as value,
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
group by start
order by start ;
