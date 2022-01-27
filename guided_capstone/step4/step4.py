#step 2
import findspark
from pyspark.sql import SparkSession
import time
import decimal
from datetime import datetime 
from pyspark.sql.types import StructType, StructField, StringType, DateType, TimestampType, IntegerType, DecimalType
import os, fnmatch
import json

findspark.init()
spark = SparkSession.builder.master('local').appName('app').getOrCreate()
spark.conf.set(
"fs.azure.account.key.aoopenendedcaptstone.blob.core.windows.net",
"GuVfKgtb2AvI7229kkslwd2PpQC69IwOzo/sO2yN8O4ztAZhRwQR7j4Tq+JeVD9aYmZPH/8Qaqt+w8OknP4OOQ=="
)

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

raw_csv = spark.sparkContext.textFile("wasbs://mycontainer@aoopenendedcaptstone.blob.core.windows.net/data/csv/*/NYSE/*.txt")
raw_json = spark.sparkContext.textFile("wasbs://mycontainer@aoopenendedcaptstone.blob.core.windows.net/data/json/*/NASDAQ/*.txt")
folder = "wasbs://output@aoopenendedcaptstone.blob.core.windows.net/"

parsed_csv = raw_csv.map(lambda line: parse_csv(line))
csv_data = spark.createDataFrame(parsed_csv, schema=schema)
csv_data.write.partitionBy("partition").mode("overwrite").parquet(f'{folder}step2_output')

parsed_json = raw_json.map(lambda line: parse_json(line))
json_data = spark.createDataFrame(parsed_json, schema=schema)
json_data.write.partitionBy("partition").mode("append").parquet(f'{folder}step2_output')

# step 3
from pyspark.sql.functions import rank
from pyspark.sql.window import Window
trade_common = spark.read.parquet(f"{folder}step2_output/partition=T")
trade = trade_common.select("trade_dt", "symbol", "exchange", "event_tm",
"event_seq_nb", "arrival_tm", "trade_pr")
# remove duplicate records
windowSpec  = Window.partitionBy("trade_dt", "symbol","exchange","event_seq_nb", "event_tm").orderBy("arrival_tm")
trade = trade.withColumn("rank",rank().over(windowSpec))
trade = trade.select("trade_dt", "symbol","exchange","event_seq_nb", "event_tm","arrival_tm", "trade_pr") \
    .filter(trade.rank==1)
#trade.write.partitionBy("trade_dt").mode("append").parquet(f"{folder}output")
trade.write.partitionBy("trade_dt").mode("overwrite").parquet("wasbs://output@aoopenendedcaptstone.blob.core.windows.net/step3_trade")
quote_common = spark.read.parquet(f"{folder}step2_output/partition=Q")
quote = quote_common.select("trade_dt", "symbol", "exchange", "event_tm",
"event_seq_nb", "arrival_tm", "bid_pr", "bid_size", "ask_pr", "ask_size")
#quote.write.partitionBy("trade_dt").mode("overwrite").parquet(f"{folder}output")
quote.write.partitionBy("trade_dt").mode("overwrite").parquet("wasbs://output@aoopenendedcaptstone.blob.core.windows.net/step3_quote")

# step4
from datetime import datetime, timedelta
file_date = "2020-08-06"
trades = spark.read.parquet("wasbs://output@aoopenendedcaptstone.blob.core.windows.net/step3_trade/")
trades.createOrReplaceTempView("trades")
mov_avg_df = spark.sql("""
select trade_dt, symbol, exchange, event_tm, event_seq_nb, trade_pr,
avg(trade_pr) over (partition by symbol, exchange order by event_tm range between interval 30 minutes preceding and current row) as mov_avg_pr
from trades
where trade_dt = '{}'
""".format(file_date))
mov_avg_df.createOrReplaceTempView("temp_trade_moving_avg")
date = datetime.strptime(file_date, '%Y-%m-%d')
prev_date_str = date - timedelta(1)
last_pr_df = spark.sql("""
with temp as (
select 
    symbol
    , exchange
    , event_tm
    , event_seq_nb
    , max(event_seq_nb) over (partition by symbol, exchange) as max_event_seq_nb 
    , trade_pr
from trades 
where trade_dt = '{}')
select symbol, exchange, trade_pr as last_trade_pr
from temp
where max_event_seq_nb = event_seq_nb
""".format(prev_date_str))
last_pr_df.createOrReplaceTempView("temp_last_trade")
quotes = spark.read.parquet("wasbs://output@aoopenendedcaptstone.blob.core.windows.net/step3_quote/")
quotes.createOrReplaceTempView("quotes")
quote_union = spark.sql("""
select
    trade_dt
    , 'Q' as rec_type
    , symbol
    , event_tm
    , event_seq_nb
    , exchange
    , bid_pr
    , bid_size
    , ask_pr
    , ask_size
    , null as trade_pr
    , null as mov_avg_pr 
from quotes
union all
select 
    trade_dt
    , 'T' rec_type
    , symbol
    , event_tm
    , event_seq_nb
    , exchange
    , null as bid_pr
    , null as bid_size
    , null as ask_pr
    , null as ask_size
    , trade_pr
    , mov_avg_pr
from temp_trade_moving_avg
""")
quote_union.createOrReplaceTempView("quote_union")
quote_union_update = spark.sql("""with temp as (
select 
    q2.*
    , row_number() over (partition by q2.symbol, q2.exchange, q2.event_seq_nb order by q1.event_tm desc) as row_num
    , avg(q1.trade_pr) over (partition by q2.symbol, q2.exchange order by q1.event_tm range between interval 30 minutes preceding and current row) as last_mov_avg_pr
    , q1.trade_pr as last_trade_pr
from quote_union q1
right join quote_union q2
    on q1.symbol = q2.symbol
    and q1.exchange = q2.exchange
    and q1.event_tm < q2.event_tm
    and q1.rec_type = 'T'
)
select 
    *
    , last_trade_pr
    , last_mov_avg_pr
from temp
where row_num = 1 
and rec_type = 'Q'
and trade_dt = '{}'
order by symbol, event_tm, event_seq_nb
""".format(file_date))
quote_union_update.createOrReplaceTempView("quote_union_update")
quote_final = spark.sql("""
select 
    q.trade_dt
    , q.symbol
    , q.event_tm
    , q.event_seq_nb
    , q.exchange
    , q.bid_pr
    , q.bid_size
    , q.ask_pr
    , q.ask_size
    , q.last_trade_pr
    , q.last_mov_avg_pr
    , case when t.last_trade_pr is not null then bid_pr - t.last_trade_pr end as bid_pr_mv
    , case when t.last_trade_pr is not null then ask_pr - t.last_trade_pr end as ask_pr_mv
from
quote_union_update q
left join temp_last_trade t
    on q.symbol = t.symbol
    and q.exchange = t.exchange
order by q.symbol, q.event_tm, q.event_seq_nb
""")
quote_final.write.mode("overwrite").parquet("wasbs://output@aoopenendedcaptstone.blob.core.windows.net/step4_output/date={}".format(file_date))
