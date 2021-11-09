-- Write a SQL query that returns the total number of goals scored by each position on
-- each country’s team. Do not include positions which scored no goals.
select 
    country_name
    , posi_to_play
    , count(*) as goals
from
    goal_details g
    join soccer_country c
        on g.team_id = c.country_id
    join player_mast p
        on p.player_id = g.player_id
group by 1,2
order by 1,2;