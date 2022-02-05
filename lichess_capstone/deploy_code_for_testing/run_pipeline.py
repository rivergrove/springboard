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
import pyodbc
from urllib.parse import quote_plus
from sqlalchemy import create_engine, event
from tqdm import tqdm
import logging

logging.basicConfig(filename='logs/log_file.txt', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class Pipeline:
    def __init__(self):
        self.games_folder = 'games'
        self.moves_folder = 'moves'
    
    def set_month(self, month):
        self.month = month

    def get_month_of_data(self, month):
        return requests.get("https://database.lichess.org/standard/lichess_db_standard_rated_" + month + ".pgn.bz2")
   
    def download_data(self):
        """
        Pull lichess games for selected month. 
        Game data starts Jan 2013.
        """

        file = self.get_month_of_data(self.month)
        write_file = f'{self.month}.pgn.bz2'
        open(write_file, 'wb').write(file.content)

        print(self.month, 'data downloaded')

    def write_unzipped_pgn(self):
        # read first n lines of zipped file and make new file

        # another way to read files commented below. Should be faster by up to 40%, but doesn't have view into lines of a file.
        # filepath = "2013-01.pgn.bz2"
        # zipfile = bz2.BZ2File(filepath) # open the file
        # data = zipfile.read() # get the decompressed data
        # newfilepath = filepath[:-4] # assuming the filepath ends with .bz2
        # open(newfilepath, 'wb').write(data) # write a uncompressed file

        read_file = f'{self.month}.pgn.bz2'
        write_file = f'{self.month}.pgn'

        # read zipped file and write subset as unzipped file
        with bz2.BZ2File(read_file, "rb") as bzfin:
            with open(write_file, "wb") as fout:
                for i, line in enumerate(bzfin):
                    if i % 1000000 == 0 and i > 0: print(f'{i} lines of {read_file} read')
                    # if i == 50000000: break
                    fout.write(line) 

    def locate_eval_games(self):
        # record tuple with location of lines for games with evals

        j = 0
        k = 0
        rows_to_read = []
        eval_lines_list = []
        unzipped_file = f'{self.month}.pgn'
        eval_lines_file = f'{self.month}_eval_lines.pgn'

        with open(unzipped_file, 'r') as f:
            with open(eval_lines_file, "w") as eval_out:
                eval_lines_list.append(eval_lines_file)
                for i, line in enumerate(f):
                    if '%eval' in line: 
                        # create file with only eval lines
                        eval_out.write(line)
                        if rows_to_read == []:
                            rows_to_read.append((last_game_end+2,j+1))
                        else:
                            rows_to_read.append((last_game_end,j))
                        j = 0
                        k += 1
                    if line[0:3] in ('1. ', '1-0', '0-1', '1/2', ' 1-', ' 0-', ' 1/'):
                        last_game_end = j
                    j += 1
        print(f'{unzipped_file} has {k} games with evals')

        # create eval file
        eval_file = f'{self.month}_eval.pgn'

        with open(unzipped_file, 'r') as fin:
            with open(eval_file, "w") as fout:
                for tupl in rows_to_read:
                    for line in itertools.islice(fin, tupl[0], tupl[1]):
                        fout.write(line)
        print(f'{eval_lines_file} and {eval_file} written')

    def create_games(self, chunk_size):
        # create a games file with all games with evals
        
        self.games_list = []
        eval_file = f'{self.month}_eval.pgn'
        games_file = f'{self.month}_games.csv'
        pgn = open(eval_file)
        
        i = 0
        chunk = 1
        global games_d
        games_d = {}

        with open(eval_file, 'r') as f:
            while True:
                file = f'{self.games_folder}/{chunk}_{games_file}'
                with open(file, "w") as fout:
                    self.games_list.append(file)
                    # write headers
                    fout.write('game_type,game_id,utc_date,utc_time,white,black,result,white_elo,black_elo,termination\n')                             

                    for j in range(1,chunk_size+1):
                        # games data
                        headers = chess.pgn.read_headers(pgn)
                        if headers is None:
                            j -= 1
                            break
                        game_type = headers['Event'].split(" ")[1]
                        game_id = headers['Site'].replace("https://lichess.org/", "")
                        utc_date = headers['UTCDate']
                        utc_time = headers['UTCTime']
                        white = headers['White']
                        black = headers['Black']
                        result = headers['Result']
                        white_elo = headers['WhiteElo']
                        black_elo = headers['BlackElo']
                        termination = headers['Termination']

                        fout.write(f'{game_type},{game_id},{utc_date},{utc_time},{white},{black},{result},{white_elo},{black_elo},{termination}\n')
                        games_d[i] = game_id
                        i += 1
                    print(f'{j} games read into games file')
                chunk += 1
                if headers is None:
                    break
        print(f'games_files written with {i} rows')
        logging.info(f'games_files written with {i} rows')
        
        return games_d

    def create_moves(self, games_chunk_size, moves_chunk_size):
        # create a moves file with all moves from games with evals

        # run the create create games method. It will output a dictionary, games_d.
        self.create_games(games_chunk_size)
        
        self.moves_list = []
        eval_lines_file = f'{self.month}_eval_lines.pgn'
        moves_file = f'{self.month}_moves.csv'
        chunk = 1
        k = 0

        # moves data
        with open(eval_lines_file, 'r') as f:
            while True:
                file = f'{self.moves_folder}/{chunk}_{moves_file}'
                with open(file, "w") as fout:
                    self.moves_list.append(file)
                    # write headers
                    fout.write('game_id,move_number,move,eval,white\n')
                    for i, line in enumerate(f,1):

                        # seperate the string by " [0-9]+\. " or " [0-9]+\.\.\. "
                        split_line = re.split(" [0-9]+\. | [0-9]+\.\.\. ", line)

                        # if the file has 200+ moves skip game because we lose evals after 200 moves
                        if len(split_line) >= 400:
                            pass

                        # write to moves table
                        else:
                            for j, move in enumerate(split_line):
                                temp_d = {}
                                if j == 0: 
                                    move_value = move.split()[1]
                                else: 
                                    move_value = move.split()[0]

                                # checkmate move has no eval value; in this case set to "-"
                                try:
                                    eval_obj = re.search('\%eval (-?[0-9]+\.[0-9]+|#-?[0-9]+)', move).group(0)
                                except AttributeError: 
                                    if '#' not in move:
                                        # removing games where there are no evals, and no checkmate
                                        eval_obj = 'no_eval'
                                    eval_obj = '-'

                                eval_value = eval_obj.replace('%eval ', "")
                                if j % 2 == 0:
                                    white = 1
                                else:
                                    white = 0

                                # write move to moves file
                                fout.write(f'{games_d[k]},{j+1},{move_value},{eval_value},{white}\n') 
                        k +=1
                        if i == moves_chunk_size:
                            break
                print(f'{i} games read into moves file')
                chunk += 1
                if i != moves_chunk_size:
                    break
        print(f'moves_files written')
        logging.info(f'moves_files written')

    def load_to_postgres(self):
        
        def chunker(seq, size):
            # from http://stackoverflow.com/a/434328
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        def insert_with_progress():
            engine = create_engine('postgresql://postgres:Virginia0@localhost:5432/anthonyolund')
            list_lists = [self.games_list, self.moves_list]
            for table_list in list_lists:
                for file_name in table_list:
                    df = pd.read_csv(file_name)
                    table_name = file_name[-9:-4]
                    chunksize = int(len(df) / 100)
                    with tqdm(total=len(df)) as pbar:
                        for i, cdf in enumerate(chunker(df, chunksize)):
                            cdf.to_sql(table_name, engine, index=False, if_exists='append')
                            pbar.update(chunksize)
                    print(f'{file_name} inserted to postgres')
        
        insert_with_progress()
        logging.info(f'{self.month} data written to postgres')
 
    def run_pipeline(self, start_year, start_month, end_year, end_month):

        start = datetime.datetime(start_year, start_month, 1)
        end = datetime.datetime(end_year, end_month, 1)
        months_range = pd.date_range(start,end, freq='MS').strftime("%Y-%m").tolist()

        # execute extracting and cleaning steps on each month of data
        for month in months_range:
            self.set_month(month)
            self.download_data()
            self.write_unzipped_pgn()
            self.locate_eval_games()
            self.create_moves(10000,10000)
            self.load_to_postgres()
            print("")

    def test_logging(self):
        logging.info('info')
        logging.warning('warn')
        logging.exception('exception')
        logging.debug('debug')