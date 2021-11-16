-- 3. List the names of students who have taken course v4 (crsCode).
/* The previous query has 8 steps in the explain statement including "materialize
with deduplication". We can bring that down to 4 steps with less total cost using
a join. */
SELECT name 
FROM Student 
join Transcript 
on Student.id = Transcript.studId 
WHERE crsCode = 'MGT382';