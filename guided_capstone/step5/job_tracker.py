import datetime
import psycopg2
from datetime import date

class Tracker(object):
    """
    job_id, status, updated_time
    """
    def __init__(self, job_name):
        self.job_name = job_name

    def assign_job_id(self):
        # [Construct the job ID and assign to the return variable]
        job_id = f'{self.job_name}_{date.today().strftime("%Y-%m-%d")}'
        return job_id

    def update_job_status(self, status):

        job_id = self.assign_job_id()
        print("Job ID Assigned: {}".format(job_id))
        update_time = datetime.datetime.now()
        conn = self.get_db_connection()

        try:
            # [Execute the SQL statement to insert to job status table]
            cur = conn.cursor()
            insert = f'''insert into guided_capstone_job_tracker (id, status, updated_at) values ('{job_id}', '{status}', '{update_time}');'''   
            cur.execute(insert)
            conn.commit()
            conn.close()
            print(f'Updated job status to {status}')
        except (Exception, psycopg2.Error) as error:
            print("error executing db statement for job tracker.")
        return

    def get_job_status(self, job_id):
        # connect db and send sql query
        conn = self.get_db_connection()
        try:
            cur = conn.cursor()
            query_string = f'''
                        select status 
                        from guided_capstone_job_tracker
                        where id = '{self.assign_job_id()}';
                        '''
            cur.execute(query_string)
            record = cur.fetchone()
            conn.close()
            return record
        except (Exception, psycopg2.Error) as error:
            print("error executing db statement for job tracker.")
        return

    def get_db_connection(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(
                    host="localhost",
                    database="postgres",
                    user="postgres",
                    password="virginia0")
            
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
    
    def select_from_tracker_table(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute('''select * from guided_capstone_job_tracker order by updated_at desc''')
        print(cur.fetchall())
        conn.close()