-- Write a SQL query to find the referees who booked the most number of players.
select 
    m.referee_id
    , r.referee_name
    , count(*) as bookings
from
    player_booked pb
    join match_mast m
        on pb.match_no = m.match_no
    join referee_mast r
        on m.referee_id = r.referee_id
group by 1,2
order by 3 desc;