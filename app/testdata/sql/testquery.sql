/*select min(id) as minid,
min(start) as minstart,
avg(cost) as cost,
avg(value) as value
from data_view
where owner = 1

group by hour
order by minstart
 */

select min(id) as minid,
min(start) as minstart,
avg(cost) as cost,
avg(value) as value,
hour
from data_view
where owner = 1

group by hour
order by minstart
