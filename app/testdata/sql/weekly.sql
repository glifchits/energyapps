/*
select start, value, cost
from data_view
where owner = 2
and start >= '2013-12-01'::date;
*/

select interval.id, reading_id, start, cost, value, eui
from interval
inner join meter_reading
  on meter_reading.id = interval.reading_id
inner join eui
  on eui.id = meter_reading.eui
where owner = 2
and start >= '2013-12-11'::date;

