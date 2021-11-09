-- Write a SQL query to find referees and the number of matches they worked in each venue.
select 
    m.referee_id
    , r.referee_name
    , v.venue_name
    , count(distinct m.match_no) as matches
from
    match_mast m
    join referee_mast r
        on m.referee_id = r.referee_id
    join soccer_venue v
        on v.venue_id = m.venue_id
group by 1,2,3;