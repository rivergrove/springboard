-- Write a SQL query to compute a list showing the number of substitutions that
-- happened in various stages of play for the entire tournament.
select time_in_out, count(*) as players
from player_in_out
where in_out = 'O'
group by 1
order by 1;