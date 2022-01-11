import decimal
from datetime import datetime 
from arrival_time import arrival_time

def parse_csv(line:str):
    record_type_pos = 2
    record = line.split(",")
    try:
        # [logic to parse records]
        if record[record_type_pos] == "T":
            event = [datetime.strptime(record[0], '%Y-%m-%d').date(),
                     record[2],
                     record[3],
                     record[6],
                     datetime.strptime(record[4], '%Y-%m-%d %H:%M:%S.%f'),
                     int(record[5]),
                     arrival_time(),
                     decimal.Decimal(record[8]),
                     None,
                     None,
                     None,
                     None,
                     record[2],
                     None]
            return event
        elif record[record_type_pos] == "Q":
            event = [datetime.strptime(record[0], '%Y-%m-%d').date(),
                     record[2],
                     record[3],
                     record[6],
                     datetime.strptime(record[4], '%Y-%m-%d %H:%M:%S.%f'),
                     int(record[5]),
                     arrival_time(),
                     None,
                     decimal.Decimal(record[7]),
                     int(record[8]),
                     decimal.Decimal(record[9]),
                     int(record[10]),
                     record[2], 
                     None]
            return event
    except Exception as e:
        # [save record to dummy event in bad partition]
        # [fill in the fields as None or empty string]
        return [None,None,None,None,None,None,None,None,None,None,None,None,record[2],line]