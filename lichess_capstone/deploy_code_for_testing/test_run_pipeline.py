from unittest import TestCase
from unittest.mock import patch, Mock
import run_pipeline
from pathlib import Path
import psycopg2

class TestPipeline(TestCase):
    @patch("requests.get")
    def test_get_month_of_data(self, mock_request: Mock):
        mock_request.return_value = 200
        p = run_pipeline.Pipeline()
        p.get_month_of_data('2013-01')
        mock_request.assert_called_once_with("https://database.lichess.org/standard/lichess_db_standard_rated_2013-01.pgn.bz2")

    def test_write_unzipped_pgn(self):
        p = run_pipeline.Pipeline()
        month = '2013-01'
        p.set_month(month)
        p.download_data()
        p.write_unzipped_pgn()
        # unzipped file
        path = Path(f'{month}.pgn')
        assert path.is_file()

    def test_locate_eval_games(self):
        p = run_pipeline.Pipeline()
        month = '2013-01'
        p.set_month(month)
        p.locate_eval_games()
        # eval lines file
        path = Path(f'{month}_eval_lines.pgn')
        assert path.is_file()
        # eval file
        path = Path(f'{month}_eval.pgn')
        assert path.is_file()

    def test_create_games(self):
        p = run_pipeline.Pipeline()
        month = '2013-01'
        games_folder = 'games'
        p.set_month(month)
        p.create_games(200)
        # games file
        for i in range(1,4):
            path = Path(f'{games_folder}/{i}_{month}_games.csv')
            assert path.is_file()
        path = Path(f'{games_folder}/4_{month}_games.csv')
        self.assertFalse(path.is_file())

    def test_create_moves(self):
        p = run_pipeline.Pipeline()
        month = '2013-01'
        moves_folder = 'moves'
        p.set_month(month)
        p.create_moves(200,200)
        # games file
        for i in range(1,4):
            path = Path(f'{moves_folder}/{i}_{month}_moves.csv')
            assert path.is_file()
        path = Path(f'{moves_folder}/4_{month}_moves.csv')
        self.assertFalse(path.is_file())

    def get_db_connection(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(
                    host="localhost",
                    database="anthonyolund",
                    user="postgres",
                    password="Virginia0")
            
            # create a cursor
            cur = conn.cursor()
            
            # create job table
            cur.execute('''
                        create table if not exists guided_capstone_job_tracker(
                            id varchar(100) primary key,
                            status varchar(10),
                            updated_at timestamp
                        )''')
            conn.commit()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return conn
 
    def select_from_tracker_table(self, query):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall(), conn

    def delete_from_tracker_table(self, table):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute(f'delete from {table};')
        conn.commit()
        conn.close()

    def test_insert_with_progress(self):
        p = run_pipeline.Pipeline()
        month = '2013-01'
        moves_folder = 'moves'
        p.set_month(month)
        p.create_moves(1000,1000)
        p.load_to_postgres()
        results, conn = self.select_from_tracker_table("select count(*) from moves;")
        conn.close()
        assert results == [(34475,)]
        results, conn = self.select_from_tracker_table("select count(*) from games;")
        conn.close()
        assert results == [(518,)]
        # close delete added records
        self.delete_from_tracker_table("moves")
        self.delete_from_tracker_table("games")