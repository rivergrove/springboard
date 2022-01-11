import decimal
from datetime import datetime 
import json
from arrival_time import arrival_time

def parse_json(line:str):
    record = json.loads(line)
    try:
        # [logic to parse records]
        if record["event_type"] == "T":
            event = [datetime.strptime(record["trade_dt"], '%Y-%m-%d').date(),
                     record["event_type"],
                     record["symbol"],
                     record["exchange"],
                     datetime.strptime(record["event_tm"], '%Y-%m-%d %H:%M:%S.%f'),
                     int(record["event_seq_nb"]),
                     arrival_time(),
                     decimal.Decimal(record["price"]),
                     None,
                     None,
                     None,
                     None,
                     record["event_type"],
                     None]
            return event
        elif record["event_type"] == "Q":
            event = [datetime.strptime(record["trade_dt"], '%Y-%m-%d').date(),
                     record["event_type"],
                     record["symbol"],
                     record["exchange"],
                     datetime.strptime(record["event_tm"], '%Y-%m-%d %H:%M:%S.%f'),
                     int(record["event_seq_nb"]),
                     arrival_time(),
                     None,
                     decimal.Decimal(record["bid_pr"]),
                     int(record["bid_size"]),
                     decimal.Decimal(record["ask_pr"]),
                     int(record["ask_size"]),
                     record["event_type"], 
                     None]
            return event
    except Exception as e:
        # [save record to dummy event in bad partition]
        # [fill in the fields as None or empty string]
        return [None,None,None,None,None,None,None,None,None,None,None,None,record[2],line]