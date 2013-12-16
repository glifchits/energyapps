select 
  sum(cost) as cost,
  sum(value) as value
from data_view
where owner = 2
and start >= '2012-12-7'::date
and start < '2012-12-14'::date
