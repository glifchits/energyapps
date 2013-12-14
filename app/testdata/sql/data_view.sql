create view data_view
as

select
  interval.id,
  eui.owner,
  interval.start,
  interval.cost,
  interval.value,
  date_part('year', start) as year,
  date_part('month', start) as month,
  date_part('day', start) as day,
  date_part('hour', start) as hour
from interval
inner join meter_reading
  on meter_reading.id = interval.reading_id
inner join eui
  on eui.id = meter_reading.eui
where meter_reading.kind = 12
order by start ;
