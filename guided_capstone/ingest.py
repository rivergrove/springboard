# step 2: data ingestions
import findspark
from pyspark.sql import SparkSession
import time
import decimal
from datetime import datetime 
from pyspark.sql.types import StructType, StructField, StringType, DateType, TimestampType, IntegerType, DecimalType
import os, fnmatch
import json
import job_tracker

findspark.init()
spark = SparkSession.builder.master('local').appName('app').getOrCreate()
spark.conf.set(
"fs.azure.account.key.aoopenendedcaptstone.blob.core.windows.net",
"GuVfKgtb2AvI7229kkslwd2PpQC69IwOzo/sO2yN8O4ztAZhRwQR7j4Tq+JeVD9aYmZPH/8Qaqt+w8OknP4OOQ=="
)

track = job_tracker.Tracker("ingest")

try:
    def parse_csv(line:str):
        record_type_pos = 2
        record = line.split(",")
        try:
            # [logic to parse records]
            if record[record_type_pos] == "T":
                event = [datetime.strptime(record[0], '%Y-%m-%d').date(),
                         record[2],
                         record[3],
                         record[6],
                         datetime.strptime(record[4], '%Y-%m-%d %H:%M:%S.%f'),
                         int(record[5]),
                         datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S.%f'),
                         decimal.Decimal(record[8]),
                         None,
                         None,
                         None,
                         None,
                         record[2],
                         None]
                return event
            elif record[record_type_pos] == "Q":
                event = [datetime.strptime(record[0], '%Y-%m-%d').date(),
                         record[2],
                         record[3],
                         record[6],
                         datetime.strptime(record[4], '%Y-%m-%d %H:%M:%S.%f'),
                         int(record[5]),
                         datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S.%f'),
                         None,
                         decimal.Decimal(record[7]),
                         int(record[8]),
                         decimal.Decimal(record[9]),
                         int(record[10]),
                         record[2], 
                         None]
                return event
        except Exception as e:
            # [save record to dummy event in bad partition]
            # [fill in the fields as None or empty string]
            return [None,None,None,None,None,None,None,None,None,None,None,None,record[2],line]

    def parse_json(line:str):
        record = json.loads(line)
        try:
            # [logic to parse records]
            if record["event_type"] == "T":
                event = [datetime.strptime(record["trade_dt"], '%Y-%m-%d').date(),
                         record["event_type"],
                         record["symbol"],
                         record["exchange"],
                         datetime.strptime(record["event_tm"], '%Y-%m-%d %H:%M:%S.%f'),
                         int(record["event_seq_nb"]),
                         datetime.strptime(record["file_tm"], '%Y-%m-%d %H:%M:%S.%f'),
                         decimal.Decimal(record["price"]),
                         None,
                         None,
                         None,
                         None,
                         record["event_type"],
                         None]
                return event
            elif record["event_type"] == "Q":
                event = [datetime.strptime(record["trade_dt"], '%Y-%m-%d').date(),
                         record["event_type"],
                         record["symbol"],
                         record["exchange"],
                         datetime.strptime(record["event_tm"], '%Y-%m-%d %H:%M:%S.%f'),
                         int(record["event_seq_nb"]),
                         datetime.strptime(record["file_tm"], '%Y-%m-%d %H:%M:%S.%f'),
                         None,
                         decimal.Decimal(record["bid_pr"]),
                         int(record["bid_size"]),
                         decimal.Decimal(record["ask_pr"]),
                         int(record["ask_size"]),
                         record["event_type"], 
                         None]
                return event
        except Exception as e:
            # [save record to dummy event in bad partition]
            # [fill in the fields as None or empty string]
            return [None,None,None,None,None,None,None,None,None,None,None,None,'B',line]
        
    schema = StructType([StructField("trade_dt", DateType(), True),
                       StructField("rec_type", StringType(), True),
                       StructField("symbol", StringType(), True),
                       StructField("exchange", StringType(), True),
                       StructField("event_tm", TimestampType(), True),
                       StructField("event_seq_nb", IntegerType(), True),
                       StructField("arrival_tm", TimestampType(), True),
                       StructField("trade_pr", DecimalType(), True),
                       StructField("bid_pr", DecimalType(), True),
                       StructField("bid_size", IntegerType(), True),
                       StructField("ask_pr", DecimalType(), True),
                       StructField("ask_size", IntegerType(), True),
                       StructField("partition", StringType(), True),
                       StructField("meta_data", StringType(), True)])

    raw_csv = spark.sparkContext.textFile("wasbs://mycontainer@aoopenendedcaptstone.blob.core.windows.net/data/csv/*/NYSE/*.txt")
    raw_json = spark.sparkContext.textFile("wasbs://mycontainer@aoopenendedcaptstone.blob.core.windows.net/data/json/*/NASDAQ/*.txt")
    folder = "wasbs://output@aoopenendedcaptstone.blob.core.windows.net/"

    parsed_csv = raw_csv.map(lambda line: parse_csv(line))
    csv_data = spark.createDataFrame(parsed_csv, schema=schema)
    csv_data.write.partitionBy("partition").mode("overwrite").parquet(f'{folder}step2_output')

    parsed_json = raw_json.map(lambda line: parse_json(line))
    json_data = spark.createDataFrame(parsed_json, schema=schema)
    json_data.write.partitionBy("partition").mode("append").parquet(f'{folder}step2_output')

    track.update_job_status("success")

except Exception as e:
    print(e)
    track.update_job_status("failed")