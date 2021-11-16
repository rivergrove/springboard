-- 2. List the names of students with id in the range of v2 (id) to v3 (inclusive).
/* 
Using the numbers directly in the query so we don't use the cache. 
Normally between would use the index, but in MySQL because we are querying
for a large percent of the rows and a full table scan requires fewer seeks, 
it will use the full table scan. 
*/
SELECT name FROM Student WHERE id BETWEEN 1145072 AND 1828467;