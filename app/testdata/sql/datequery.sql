select min(id), sum(cost), date_part('month', start) as month 
from interval

where start >= '2012-01-01'::date
and start < '2012-06-01'::date

group by month
