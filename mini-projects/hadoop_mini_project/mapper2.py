#!/usr/bin/env python

import sys
# input comes from STDIN (standard input)
i = 0
for line in sys.stdin:
    row = line.split('\t')
    key = row[1].strip('\n')
        
    print(key + ' 1')