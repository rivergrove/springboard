!pip3 install chess
import requests
import datetime 
from dateutil.relativedelta import relativedelta
import bz2
import pandas as pd
import itertools
import zipfile
import json, os
import chess.pgn
import re
import numpy as np
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, StringType, DateType, TimestampType, IntegerType, DecimalType
from pyspark.sql.window import Window

spark = SparkSession.builder.master('local').appName('app').getOrCreate()
spark.conf.set(
"fs.azure.account.key.aoopenendedcaptstone.blob.core.windows.net",
"GuVfKgtb2AvI7229kkslwd2PpQC69IwOzo/sO2yN8O4ztAZhRwQR7j4Tq+JeVD9aYmZPH/8Qaqt+w8OknP4OOQ=="
)
spark.sparkContext.setLogLevel("OFF")
spark.conf.set("spark.sql.adaptive.enabled", "true")

class Pipeline:
    def __init__(self):
        pass
    
    def download_data(self, month):
        """
        Pull lichess games for selected month. 
        Game data starts Jan 2013.
        """
        
        mount = '/dbfs/mnt/iotdata/'
        file = requests.get("https://database.lichess.org/standard/lichess_db_standard_rated_" + month + ".pgn.bz2")
        write_file = f'{mount}{month}.pgn.bz2'
        open(write_file, 'wb').write(file.content)

        print(f'{month}: data downloaded')

    def create_games(self, month):
        # create a game files with all games with evals
        raw_data = spark.sparkContext.textFile(f"dbfs:/mnt/iotdata/{month}.pgn.bz2")
        data_list = raw_data.collect()
        print(f"{month}: raw data collected")
        
        df = spark.createDataFrame(data_list, StringType())
        # free up memory
        del raw_data, data_list
        df = df.filter(df.value!="").withColumn("id", F.monotonically_increasing_id())
        df.createOrReplaceTempView("raw_data")
        df = spark.sql("with ordered_data as (select value, id, case when substr(value, 1, 6) = '[Event' then 1 else 0 end as new_game from raw_data), \
             game_data as (select *, sum (new_game) OVER (order by id) as game_id from ordered_data) \
             select *, max(id) over (partition by game_id) = id as move_row from game_data")
        df.createOrReplaceTempView("ordered_data")
        eval_games = spark.sql("select game_id from ordered_data where move_row = true and value like '%eval%'")
        eval_games.createOrReplaceTempView("eval_games")
        eval_df = spark.sql("select * from ordered_data where game_id in (select game_id from eval_games)")
        eval_df.createOrReplaceTempView("eval_data")
        df = spark.sql("select game_id, \
            max(case when substr(value, 2, 5)='Event' then value end) as event, \
            max(case when substr(value, 2, 4)='Site' then value end) as site, \
            max(case when substr(value, 2, 7)='UTCDate' then value end) as utc_date, \
            max(case when substr(value, 2, 7)='UTCTime' then value end) as utc_time, \
            max(case when substr(value, 2, 5)='White' then value end) as white, \
            max(case when substr(value, 2, 5)='Black' then value end) as black, \
            max(case when substr(value, 2, 6)='Result' then value end) as result, \
            max(case when substr(value, 2, 8)='WhiteElo' then value end) as white_elo, \
            max(case when substr(value, 2, 8)='BlackELo' then value end) as black_elo, \
            max(case when substr(value, 2, 11)='Termination' then value end) as termination \
            from eval_data group by 1")
        df = df.select(F.regexp_replace(F.regexp_replace(F.slice(F.split(df.event, " "),2,100).cast("string"),",", " "), "(\]|\[)|\"", "").alias("event"),
              F.regexp_replace(F.slice(F.split(df.site, " "),2,100).cast("string"), "(https://lichess.org/)|\]|\[|\"", "").alias("url"),
              F.regexp_replace(F.slice(F.split(df.utc_date, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("utc_date"),
              F.regexp_replace(F.slice(F.split(df.utc_time, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("utc_time"),
              F.regexp_replace(F.slice(F.split(df.white, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("white"),
              F.regexp_replace(F.slice(F.split(df.black, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("black"),
              F.regexp_replace(F.slice(F.split(df.result, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("result"),
              F.regexp_replace(F.slice(F.split(df.white_elo, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("white_elo"),
              F.regexp_replace(F.slice(F.split(df.black_elo, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("black_elo"),
              F.regexp_replace(F.slice(F.split(df.termination, " "),2,100).cast("string"), "(\]|\[)|\"", "").alias("termination"))
        print(f'{month}: games cleaned')
        
        df.write.mode("overwrite").parquet('dbfs:/mnt/iotdata/')
        print(f'{month}: {df.count()} games written')

    def create_moves(self, month):
        # create a moves file with all moves from games with evals

        game_urls = spark.sql("select game_id, max(case when substr(value, 2, 4)='Site' then right(left(value, length(value) - 2), length(value) - length('[Site *https://lichess.org/') - 2) end) as url from eval_data where group by 1")
        game_urls.createOrReplaceTempView("game_urls")
        raw_moves = spark.sql("select ed.value, gu.url from eval_data ed join game_urls gu on ed.game_id = gu.game_id where move_row = true")
        # delete eval_data for QA
        spark.catalog.dropTempView("eval_data")

        # split moves line into array of moves
        # filter out games with 400+ moves because they stop recording evals
        # split array into 1 row per move
        moves_exploded = raw_moves.withColumn(
            "split_line",
            F.split(raw_moves.value, " [0-9]+\. | [0-9]+\.\.\. ")
        ).filter(F.size(F.col("split_line")) < 400).withColumn("move", F.explode("split_line")).withColumn("id", F.monotonically_increasing_id()).select("move", "url","id")

        # remove move number from first move of every game
        # split move into eval and move
        formatted_moves = moves_exploded.withColumn("move", F.when(F.expr("substring(move, 1, 3)") == "1. ", F.expr("substring(move, 4, length(move) - 3)")).otherwise(moves_exploded.move)).withColumn("eval",F.regexp_extract("move", '\%eval (-?[0-9]+\.[0-9]+|#-?[0-9]+)', 1)).withColumn("move",F.split("move"," ")[0])
        
        # add move_number and white
        windowSpec = Window.partitionBy("url").orderBy("id")
        clean_moves = formatted_moves.withColumn("move_number",F.row_number().over(windowSpec)).withColumn("white", F.when(F.col("move_number") % 2 == 1, True).otherwise(False)).orderBy("id").drop("id")
        clean_moves.createOrReplaceTempView("clean_moves")

        # drop games with missing evals
        games_to_drop = formatted_moves.filter("eval is null").select("url").distinct()
        games_to_drop.createOrReplaceTempView("games_to_drop")
        print(f'{games_to_drop.count()} games with missing evals')
        filtered_moves = spark.sql("select m.* from clean_moves as m left join games_to_drop as d on m.url = d.url where d.url is null")
        print(f'{filtered_moves.count()} moves to upload')
        
        filtered_moves.write.mode("overwrite").parquet('dbfs:/mnt/iotdata/')

#         clean_moves.write.mode("overwrite").parquet('dbfs:/mnt/iotdata/')
        print(f'{month}: moves written')

    def run_pipeline(self, start_year, start_month, end_year, end_month):

        start = datetime.datetime(start_year, start_month, 1)
        end = datetime.datetime(end_year, end_month, 1)
        months_range = pd.date_range(start,end, freq='MS').strftime("%Y-%m").tolist()

        # execute extracting and cleaning steps on each month of data
        for month in months_range:
            self.download_data(month)
            self.create_games(month)
            self.create_moves(month)
            print("")

    def test_logging(self):
        logging.info('info')
        logging.warning('warn')
        logging.exception('exception')
        logging.debug('debug')