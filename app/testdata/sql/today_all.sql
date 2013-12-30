select 
  start,
  'value' as type,
  cost,
  value
from (
  select start, cost, value
  from data_view
  where owner = 9
  order by start desc
  limit 24
) as query
union
select 
  min(start) as start,
  'aggregate' as type,
  avg(cost) as cost,
  avg(value) as value
from data_view
where owner = 9
group by hour

order by type, start
