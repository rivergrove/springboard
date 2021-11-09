--  Write a SQL query to find all available information about the players under contract to
-- Liverpool F.C. playing for England in EURO Cup 2016.
select 
    p.*
from
    player_mast p
    join soccer_country c
        on p.team_id = c.country_id
        and country_abbr = 'ENG'
where
    playing_club = 'Liverpool'