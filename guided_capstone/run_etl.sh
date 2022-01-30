path="/Users/anthonyolund/documents/dev/apache-spark/spark-3.2.0-bin-hadoop3.2/bin/"
tracker="/Users/anthonyolund/Dropbox/Code/springboard/spark_test/guided_capstone/job_tracker.py"
submit="${path}spark-submit"
eval "$submit" ingest.py \
--py-files "$tracker"

eval "$submit" optimize_code_performance.py \
--py-files "$tracker"

eval "$submit" analytical_etl.py \
--py-files "$tracker"