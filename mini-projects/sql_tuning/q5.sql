-- 5. List the names of students who have taken a course from department v6 (deptId), but not v7.
/*
I don't see major improvements to this query. I could add an index to course for the
department id but I don't think that's an intutive index as it's not a primary key.
Most of the cost is on the join between course and transcript, but I don't see
an obvious way to speed that up. 
*/
SELECT * FROM Student, 
    (SELECT studId FROM Transcript, Course WHERE deptId = 'MGT' AND Course.crsCode = Transcript.crsCode
    AND studId NOT IN
    (SELECT studId FROM Transcript, Course WHERE deptId = 'EE' AND Course.crsCode = Transcript.crsCode)) as alias
WHERE Student.id = alias.studId;