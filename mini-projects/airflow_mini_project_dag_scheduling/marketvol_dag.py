from datetime import timedelta, datetime
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import yfinance as yf

args={    
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    dag_id='marketvol',
    default_args=args,
    schedule_interval="0 18 * * 1-5", # 6pm M-F
    start_date=datetime.today()
)

create_data_directory = BashOperator(
    task_id="create_data_directory",
    bash_command="mkdir -p /tmp/data/{{ds}}",
    dag=dag
)

folder = f"/tmp/data/{str(datetime.today().date())}/"

def download_stock_data(symbol, start_date, end_date):
    data_df = yf.download(symbol, start=start_date, end=end_date, interval='1m')
    #data_df = yf.download(symbol, start='2022-01-13', end='2022-01-14', interval='1m')
    data_df.to_csv(f"{folder}{symbol}.csv", header=False)
    print(f'start_date: {start_date}, end_date: {end_date}')

start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
end_date = datetime.today()

download_tesla_data = PythonOperator(
    task_id="download_tesla_data",
    python_callable=download_stock_data,
    op_kwargs={'symbol':'TSLA', 
               'start_date': start_date,
               'end_date': end_date}
)

download_apple_data = PythonOperator(
    task_id="download_apple_data",
    python_callable=download_stock_data,
    op_kwargs={'symbol':'AAPL',
               'start_date':start_date,
               'end_date':end_date}
)

load_tesla_to_hdfs = BashOperator(
    task_id="load_tesla_to_hdfs",
    bash_command="hdfs dfs -put /tmp/data/{{ds}}/TSLA.csv /data/TSLA_{{ds}}.csv",
    dag=dag
)

load_apple_to_hdfs = BashOperator(
    task_id="load_apple_to_hdfs",
    bash_command="hdfs dfs -put /tmp/data/{{ds}}/AAPL.csv /data/AAPL_{{ds}}.csv",
    dag=dag
)

query_data = BashOperator(
    task_id="query_data",
    bash_command="hdfs dfs -head /data/TSLA_{{ds}}.csv && hdfs dfs -head /data/AAPL_{{ds}}.csv",
    dag=dag
)

create_data_directory >> download_tesla_data >> load_tesla_to_hdfs >> query_data
create_data_directory >> download_apple_data >> load_apple_to_hdfs >> query_data


