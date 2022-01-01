#!/usr/bin/env python

import sys

def flush(make, year, l):
    # [Write the output]
    for entry in l:
        text = entry + '\t' + make + ',' + year
        # text = '%s\t%s,%s' % (entry, make, year)
        print(text.strip('\n'))
l = []
current_vin = None
for line in sys.stdin:
    # [parse the input we got from mapper and update the master info]
    split = line.split('\t')
    vin = split[0]
    incident_type = split[1].split(',')[0]
    make = split[1].split(',')[1]
    year = split[1].split(',')[2]

    # [detect key changes]
    if current_vin != vin:
        if current_vin != None:
            # write result to STDOUT
            flush(master_make, master_year,l)
        # reset()
        l = []
        master_year = ''
        master_make = ''
    if incident_type == 'A':
        l.append(vin)

    # if there is a make and year, record it
    if make and year:
        master_make = make
        master_year = year

    # [update more master info after the key change handling]
    current_vin = vin
# do not forget to output the last group if needed!
flush(master_make, master_year,l)