-- 4. List the names of students who have taken a course taught by professor v5 (name).
/* update the where clause to search for professor by id rather than name
create index on professor id */
create index professor_id on Professor(id);
SELECT name FROM Student,
    (SELECT studId FROM Transcript,
        (SELECT crsCode, semester FROM Professor
            JOIN Teaching
            WHERE Professor.id = 3148201 AND Professor.id = Teaching.profId) as alias1
    WHERE Transcript.crsCode = alias1.crsCode AND Transcript.semester = alias1.semester) as alias2
WHERE Student.id = alias2.studId;