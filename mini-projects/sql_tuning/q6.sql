-- 6. List the names of students who have taken all courses offered by department v8 (deptId).
-- created an index to speed up teaching
create index teaching_all on teaching(crsCode,profId,semester);
explain analyze SELECT name FROM Student,
    (SELECT studId
    FROM Transcript
        WHERE crsCode IN
        (SELECT crsCode FROM Course WHERE deptId = 'MAT' AND crsCode IN (SELECT crsCode FROM Teaching))
        GROUP BY studId
        HAVING COUNT(*) = 
            (SELECT COUNT(*) FROM Course WHERE deptId = 'MAT' AND crsCode IN (SELECT crsCode FROM Teaching))) as alias
WHERE id = alias.studId;