-- Write a SQL query to find all the venues where matches with penalty shootouts were played
select sv.venue_name
from match_mast m
join soccer_venue sv
    on m.venue_id = sv.venue_id
    and decided_by = 'P';