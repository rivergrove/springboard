-- 1. List the name of the student with id equal to v1 (id).
-- create index and reference v1 directly rather than using cache.
create index student_id on student(id);
SELECT name FROM Student WHERE id = 1612521;