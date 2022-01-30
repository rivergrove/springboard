# step 3: Optimizing Code Performance
from pyspark.sql.functions import rank
from pyspark.sql.window import Window
import findspark
from pyspark.sql import SparkSession
import job_tracker

findspark.init()
spark = SparkSession.builder.master('local').appName('app').getOrCreate()
spark.conf.set(
"fs.azure.account.key.aoopenendedcaptstone.blob.core.windows.net",
"GuVfKgtb2AvI7229kkslwd2PpQC69IwOzo/sO2yN8O4ztAZhRwQR7j4Tq+JeVD9aYmZPH/8Qaqt+w8OknP4OOQ=="
)

track = job_tracker.Tracker("optimize_code_performance")

try:
    folder = "wasbs://output@aoopenendedcaptstone.blob.core.windows.net/"
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

    track.update_job_status("success")

except Exception as e:
    print(e)
    track.update_job_status("failed")
