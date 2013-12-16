/*
select
 avg(value) as value,
 avg(cost) as cost
from (
*/
    /*
  select 
    min(id) as id,
    min(start) as start,
    avg(value) as value,
    avg(cost) as cost
    id,
    start,
    value,
    cost
  from data_view
  where owner = 2
  --group by year, month, day
  order by start asc
--) as avg_by_day
    */

select 
  avg(value) as value,
  avg(cost) as cost
from (
  select 
    min(id) as id,
    min(start) as start,
    sum(value) as value,
    sum(cost) as cost,
    div(cast(day as integer), 7) as week
  from data_view
  where owner = 2
  -- can't include week 4, half weeks
  and day < 28
  group by year, month, week
) as avg_by_week

