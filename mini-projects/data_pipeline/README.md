# Instructions
The following file provides instructions how to run the provided scripts to ingest csv data to mysql. Please follow the steps below.

1. Install mysql and create the ticket_sales_event table using the create_ticket_sales_event.sql script provided.
2. Install mysql python connector using the following terminal command: pip3 install mysql-connector-python
3. Set up your connection using the get_db_connection() function in the pipeline.py file. If you need the hostname, run select @@hostname;. If you need the user_name run select user();.
4. Edit the database name both in the connection function and in the insert statement. 
5. Run the load_third_party() function with file_path_csv set to where you have the file stored. 
6. Run query_popular_tickets()
