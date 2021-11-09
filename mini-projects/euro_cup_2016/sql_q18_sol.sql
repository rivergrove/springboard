-- Write a SQL query to find the highest number of foul cards given in one match.
select 
    match_no
    , count(*) foul_cards
from
    player_booked pb
group by 1
order by 2 desc
limit 1;