select 
  max(start) as last_start,
  max(day) as last_day,
  max(hour) as last_hour,
  sum(value),
  date_part('days',
    date_trunc('month', max(start))
    + '1 month'::interval
    - date_trunc('month', max(start))
  ) as days
from data_view
where owner = 2
and start >= '2013-12-01'::date
group by month


