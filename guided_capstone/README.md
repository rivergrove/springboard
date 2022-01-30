# Guided Capstone: Market ETL and Analysis 

## Step 1: Create ETL Diagram

![etl](https://github.com/rivergrove/springboard/blob/master/guided_capstone/etl_design.png)

## Step 2: Data Ingestion

[Data ingestion](https://github.com/rivergrove/springboard/blob/master/guided_capstone/ingest.py):
- Create csv and json parsers
- Create a spark schema
- Load source files from Azure blob storage and apply parsers
- Write parquet data back to blob storage

## Step 3: Optimizing Code Performance

[Optimizing code performance](https://github.com/rivergrove/springboard/blob/master/guided_capstone/optimize_code_performance.py):
- Remove duplicate records using spark windows functions
- Write data back to Azure blob storage as parquet files

## Step 4: Analytical ETL

[Analytical ETL](https://github.com/rivergrove/springboard/blob/master/guided_capstone/analytical_etl.py):
- Calculate The 30-min Moving Average Using The Spark Temp View
- Calculate Last Trade Price Using The Spark Temp View
- Populate The Latest Trade and Latest Moving Average Trade Price To The Quote Records
- Join With Table temp_last_trade To Get The Prior Day Close Price
- Write The Final Dataframe Into Azure Blob Storage At Corresponding Partition

## Step 5: Pipeline Orchestration

Run [Bash Script](https://github.com/rivergrove/springboard/blob/master/guided_capstone/run_etl.sh) for pipeline orchestration:
    
    path="/Users/anthonyolund/documents/dev/apache-spark/spark-3.2.0-bin-hadoop3.2/bin/"
    tracker="/Users/anthonyolund/Dropbox/Code/springboard/spark_test/guided_capstone/job_tracker.py"
    submit="${path}spark-submit"
    eval "$submit" ingest.py \
    --py-files "$tracker"

    eval "$submit" optimize_code_performance.py \
    --py-files "$tracker"

    eval "$submit" analytical_etl.py \
    --py-files "$tracker"
