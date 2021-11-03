import requests
import datetime
from dateutil.relativedelta import relativedelta

def download_data(start_year, start_month, end_year, end_month):
    """
    Select start year and month, and end year and month to pull lichess games for that timeframe. 
    Game data starts Jan 2013.
    """
    start = datetime.datetime(start_year, start_month, 1)
    end = datetime.datetime(end_year, end_month, 1)
    while start <= end:
        start_text = str(start.year) + "-" + f'{start.month:02}'
        file = requests.get("https://database.lichess.org/standard/lichess_db_standard_rated_" + start_text + ".pgn.bz2")
        open(start_text + ".pgn.bz2", 'wb').write(file.content)
        start += relativedelta(months=+1)