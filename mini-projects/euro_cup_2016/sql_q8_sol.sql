-- Write a SQL query to find the match number for the game with the highest number of
-- penalty shots, and which countries played that match.
with max_match as (
select match_no, count(*)
from penalty_shootout 
group by 1
order by 2 desc
limit 1
)
select
    m.match_no
    , c.country_name
from
    max_match m
    join match_details d
        on m.match_no = d.match_no
    join soccer_country c
        on c.country_id = d.team_id;