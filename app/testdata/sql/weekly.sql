select sum(value), sum(cost)
from data_view
where owner = 2
and start >= '2013-12-14'::date
and start < '2013-12-15'::date;


select hour, count(hour)
from data_view
group by hour
order by hour;
