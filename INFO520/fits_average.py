#!/usr/bin/env python
__author__ = 'senorrift'

from sys import argv

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
print composition