--  Write a SQL query to find the substitute players who came into the field in the first
-- half of play, within a normal play schedule
select 
    distinct p.player_name
from
    player_in_out io
    join player_mast p
        on io.player_id = p.player_id
where
    in_out = 'I'
    and play_half = 2
    and play_schedule = 'NT';