-- Write a SQL query to find the players, their jersey number, and playing club who were
-- the goalkeepers for England in EURO Cup 2016.
select 
    player_name
    , jersey_no
    , playing_club
from
    player_mast p
    join soccer_country c
        on p.team_id = c.country_id
        and country_abbr = 'ENG'
        and posi_to_play = 'GK';