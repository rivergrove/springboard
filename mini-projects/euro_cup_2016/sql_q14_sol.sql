-- Write a SQL query to find referees and the number of bookings they made for the
-- entire tournament. Sort your answer by the number of bookings in descending order.
select 
    m.referee_id
    , r.referee_name
    , count(*) as bookings
    , count(distinct m.match_no) as matches
from
    player_booked pb
    join match_mast m
        on pb.match_no = m.match_no
    join referee_mast r
        on m.referee_id = r.referee_id
group by 1,2
order by 3 desc;