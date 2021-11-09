-- Write a SQL query to find the country where the most assistant referees come from,
-- and the count of the assistant referees.
select 
    c.country_name
    , count(distinct ass_ref) as assistant_referees
from
    match_details m
    join asst_referee_mast r
        on m.ass_ref = r.ass_ref_id
    join soccer_country c
        on c.country_id = r.country_id
group by 1
order by 2 desc
limit 1;