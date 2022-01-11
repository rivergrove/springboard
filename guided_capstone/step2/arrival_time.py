import time
from datetime import datetime 

def arrival_time():
    date_string = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')