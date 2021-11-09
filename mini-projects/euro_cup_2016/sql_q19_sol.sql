--  Write a SQL query to find the number of captains who were also goalkeepers
select 
    count(distinct player_id) as captain_gks
from
    match_captain c
    join player_mast p
        on c.player_captain = p.player_id
        and posi_to_play = 'GK';