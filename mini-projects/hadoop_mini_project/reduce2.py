#!/usr/bin/env python

import sys

d = {}
for i, line in enumerate(sys.stdin):
    # [parse the input we got from mapper and update the master info]
    split = line.split(' ')
    make_year = split[0]

    if make_year in d:
        d[make_year] += 1
    else:
        d[make_year] = 1

for key, value in d.items():
    print(key, value)