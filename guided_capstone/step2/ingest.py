import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DateType, TimestampType, IntegerType, DecimalType
import os, fnmatch
from parse_json import parse_json
from parse_csv import parse_csv

findspark.init()
spark = SparkSession.builder.master('local').appName('app').getOrCreate()
spark.conf.set(
"fs.azure.account.key.aoopenendedcaptstone.blob.core.windows.net",
"GuVfKgtb2AvI7229kkslwd2PpQC69IwOzo/sO2yN8O4ztAZhRwQR7j4Tq+JeVD9aYmZPH/8Qaqt+w8OknP4OOQ=="
)

schema = StructType([StructField("trade_dt", DateType(), True)
                   , StructField("rec_type", StringType(), True)
                   , StructField("symbol", StringType(), True)
                   , StructField("exchange", StringType(), True)
                   , StructField("event_tm", TimestampType(), True)
                   , StructField("event_seq_nb", IntegerType(), True)
                   , StructField("arrival_tm", TimestampType(), True)
                   , StructField("trade_pr", DecimalType(), True)
                   , StructField("bid_pr", DecimalType(), True)
                   , StructField("bid_size", IntegerType(), True)
                   , StructField("ask_pr", DecimalType(), True)
                   , StructField("ask_size", IntegerType(), True)
                   , StructField("partition", StringType(), True)
                   , StructField("meta_data", StringType(), True)])

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

raw_csv = spark.sparkContext.textFile("wasbs://mycontainer@aoopenendedcaptstone.blob.core.windows.net/data/csv/*/NYSE/*.txt")
raw_json = spark.sparkContext.textFile("wasbs://mycontainer@aoopenendedcaptstone.blob.core.windows.net/data/json/*/NASDAQ/*.txt")

parsed_csv = raw_csv.map(lambda line: parse_csv(line))
csv_data = spark.createDataFrame(parsed_csv, schema=schema)
csv_data.write.partitionBy("partition").mode("overwrite").parquet(f'output_dir')

parsed_json = raw_json.map(lambda line: parse_json(line))
json_data = spark.createDataFrame(parsed_json, schema=schema)
json_data.write.partitionBy("partition").mode("append").parquet(f'output_dir')
