select
max(start) as start,
date_part('year', max(start)) as year,
date_part('month', max(start)) as month,
date_part('week', max(start)) as week,
date_part('day', max(start)) as day,
date_part('hour', max(start)) as hour,
sum(cost) as cost,
sum(value) as value,
date_part('days',
  date_trunc('month', max( start ))
  + '1 month'::interval
  - date_trunc('month', max( start ))
) as days_in_month,
extract(dow from max(start)) as day_of_week
from data_view
where owner = 9
group by year, week
order by start desc
