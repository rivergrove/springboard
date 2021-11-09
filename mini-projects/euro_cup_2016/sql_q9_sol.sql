select distinct 
    p.player_name
    , jersey_no
    , c.country_name
from player_mast p
    join match_details m
        on m.player_gk = p.player_id
        and posi_to_play = 'GK'
    join soccer_country c
        on c.country_id = m.team_id
        and country_abbr = 'GER'
where play_stage = 'G';