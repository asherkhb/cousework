#!/usr/bin/env python

from datetime import datetime
from sys import argv

__author__ = 'senorrift'
start = datetime.now()


def analyze_sorted(csv_file):
    with open(csv_file, 'r') as inpt:
        analysis = []
        header = next(inpt)
        current_type = ''
        current_count = 0
        current_contents = []
        for line in inpt:
            content = line.split(',')
            filename = content[0]
            vimtype = content[2]
            if vimtype != current_type:
                if current_type != '':
                    print "%s: %d" % (current_type, current_count)
                    analysis.append({"type": current_type,
                                     "count": current_count,
                                     "contents": current_contents})
                current_type = vimtype
                current_count = 1
                current_contents = [filename]
            else:
                current_count += 1
                current_contents.append(filename)
        analysis.append({"type": current_type,
                         "count": current_count,
                         "contents": current_contents})
        return analysis


composition = analyze_sorted(argv[1])
log = []
for group in composition:
    vimtype = group["type"]
    count = group["count"]
    content = group["contents"]
    f = content[0]
    l = content[len(content)-1]
    if vimtype == 'DARK':
        avg_name = f + "-" + l
        log.append("%s: %d\n>DARK GROUP AVERAGED: %s\n" % (vimtype, count, avg_name))
    elif vimtype == 'SCIENCE':
        log.append("%s: %d\n" % (vimtype, count))
    else:
        log.append("%s: %d\n>WARNING: UNKNOWN TYPE GROUP (SKIPPED)\n" % (vimtype, count))

end = datetime.now()
duration = end - start
print "FITS Averaging Complete"
print "Total Execution Time (seconds): %d.%d" % (duration.seconds, duration.microseconds)
print ''.join(log).rstrip('\n')