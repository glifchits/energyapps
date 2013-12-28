/*
select year, month, day
from data_view
where owner = 9
group by year, month, day
order by year desc, month desc, day desc
limit 1 offset 1
*/

select
min(start) as start,
'yesterday' as type,
sum(cost) as cost,
sum(value) as value
from data_view
where owner = 9
and (year, month, day) = (
  select year, month, day
  from data_view
  where owner = 9
  group by year, month, day
  order by year desc, month desc, day desc
  limit 1 offset 1
)
UNION
select
  min(start) as start,
  'average' as type,
  avg(cost) as cost,
  avg(value) as value
from (
  select 
    min(start) as start,
    sum(cost) as cost,
    sum(value) as value
  from data_view
  where owner = 9
  group by year, month, day
) as query
