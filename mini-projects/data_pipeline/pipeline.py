import mysql.connector
import pandas as pd

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(user='root',
        password=password, # enter valid password
        host='MacBook-Pro.local',
        port='3306',
        database='anthony')
    except Exception as error:
        print("Error while connecting to database for job tracker", error)
    return connection

def load_third_party(connection, file_path_csv):
    cursor = connection.cursor()
    # [Iterate through the CSV file and execute insert statement]
    csv_data = pd.read_csv(file_path_csv, index_col=False, delimiter = ',')
    sql = 'INSERT INTO anthony.ticket_sales_event VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    for i,row in csv_data.iterrows():
        cursor.execute(sql, tuple(row))  
        print("row inserted")            
    connection.commit()
    cursor.close()
    return

def query_popular_tickets(connection):
    # Get the most popular ticket in the past month
    sql_statement = "select event_name from (select event_name, sum(num_tickets) from ticket_sales_event group by 1 order by 1 desc limit 1) as a"
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    records = cursor.fetchall()
    print(records[0][0])
    cursor.close()
    return records

# load_third_party(get_db_connection(),"third_party_sales_1.csv")
query_popular_tickets(get_db_connection())
