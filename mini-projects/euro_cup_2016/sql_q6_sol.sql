-- Write a SQL query to find the number of matches that were won by a single point, but
-- do not include matches decided by penalty shootout.
select count(*) matches
from match_mast
where results = 'WIN' 
and decided_by = 'N'
and abs(substring(goal_score,1,1) - substring(goal_score,3,1)) = 1;