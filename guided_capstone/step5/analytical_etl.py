# step4: Analytical ETL
from datetime import datetime, timedelta
import findspark
from pyspark.sql import SparkSession
import job_tracker

findspark.init()
spark = SparkSession.builder.master('local').appName('app').getOrCreate()
spark.conf.set(
"fs.azure.account.key.aoopenendedcaptstone.blob.core.windows.net",
"GuVfKgtb2AvI7229kkslwd2PpQC69IwOzo/sO2yN8O4ztAZhRwQR7j4Tq+JeVD9aYmZPH/8Qaqt+w8OknP4OOQ=="
)

track = job_tracker.Tracker("analytical_etl")

try:
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

    track.update_job_status("success")

except Exception as e:
    print(e)
    track.update_job_status("failed")
