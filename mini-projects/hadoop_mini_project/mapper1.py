#!/usr/bin/env python
import sys
# input comes from STDIN (standard input)
for line in sys.stdin:
    # for each vin number produce incident type, make, year
    row = line.split(',')
    key = row[2]
    value = row[1] + ',' + row[3] + ',' + row[5]
    # value = (row[1], row[3], row[5])
    # [derive mapper output key values]
    
    #print '%s\t%s' % (key, value)
    print(key + '\t' + value)