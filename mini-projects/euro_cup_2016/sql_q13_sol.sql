-- Write a SQL query to find all the defenders who scored a goal for their teams
select 
    posi_to_play
    , p.player_name
    , count(*) as goal
from
    goal_details g
    join player_mast p
        on p.player_id = g.player_id
        and posi_to_play = 'DF'
group by 1,2
having count(*) = 1;