## Notes

The python script runs 100MB in 2 minutes and 1GB in 20 minutes. It appears to scale arithmetically, or with O(n) complexity. Over 50% of the runtime is in unzipping of the file. Perhaps I can multithread this to best improve performance.

The pyspark script runs 100MB in 7 minutes, and in 11 minutes if I run an extra QA check to ensure there are no rows in the moves table with no eval value. Every step of the pyspark script is slower than the plain python scipt. I was also encountering memory issues as I approached 100MB. 

At this time, I think I will go with the python script rather than the pyspark functions because it's faster across the board. I should use chunking where I write files every GB so I don't lose progress if I encounter an error. 
