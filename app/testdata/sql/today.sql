select 
  min(start) as start,
  sum(cost) as cost,
  sum(value) as value
from data_view
where owner = 9
and (year, month, day) = 
  (select year, month, day
    from data_view
    where owner = 9
    order by start desc
    limit 1)
