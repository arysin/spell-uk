#!/usr/bin/env python3

import sys

d = {}
read = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.strip() in d:
            print('Already in', line.strip(), file=sys.stderr)
        d[line.strip()] = ''
        read += 1

print('Dictionary size: ', len(d), 'read in', read, file=sys.stderr)

total = 0
leftin = 0
with open(sys.argv[2]) as f:
    for line in f:
        if not line.strip() in d:
            sys.stdout.write(line)
            leftin += 1
        total += 1

print('Total in', total, 'left', leftin, file=sys.stderr)
