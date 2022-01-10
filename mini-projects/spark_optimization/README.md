## Optimizations

I added turned on adaptive query execution using `spark.conf.set("spark.sql.adaptive.enabled","True")`. I also created 2 sql tables and ran one query that combined the join, aggregation and sort.

The run time reduce from just over 2 seconds to 1 second.
