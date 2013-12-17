select 
  min(id) as id,
  min(start) as start,
  avg(cost) as cost, avg(value) as value
from (
  select
  min(id) as id,
  min(start) as start,
  sum(cost) as cost,
  sum(value) as value
  from data_view
  where owner = 2

  group by year, month
  order by id
) as sub_query
