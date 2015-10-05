#!/usr/bin/env python

from datetime import datetime
from sys import argv

__author__ = 'senorrift'
start = datetime.now()


def analyze_sorted(csv_file):
    # TODO: Incorporate validate dark function.
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


def validate_dark(img):
    pass


def generate_log(composition):
    log = []
    for group in composition:
        vimtype = group["type"]
        count = group["count"]
        content = group["contents"]
        f = content[0].rstrip(".fits")
        l = content[len(content)-1].split("_")[1].replace(".fits", "_avg.fits")
        if vimtype == 'DARK':
            avg_name = f + "-" + l
            log.append("%s: %d\n>DARK GROUP AVERAGED: %s\n" % (vimtype, count, avg_name))
        elif vimtype == 'SCIENCE':
            log.append("%s: %d\n" % (vimtype, count))
        else:
            log.append("%s: %d\n>WARNING: UNKNOWN TYPE GROUP (SKIPPED)\n" % (vimtype, count))
    return log


def spawn_makeflow_entry(program, input_list):
    """
    Spawn Makeflow Entry.
    From a program, input, and reference, generates a makeflow entry for that input.
    Currently designed to work with 'fitssub' (LINK).

    :param program: program that will be run (i.e. 'fitssub')
    :param inputf: input FITS file (usually with VIMTYPE='SCIENCE')
    :param reference: reference FITS file (usually with VIMTYPE='DARK')
    :return: makeflow entry (str)
    """
    f = input_list[0].rstrip(".fits")
    l = input_list[len(input_list)-1].split("_")[1].replace(".fits", "_avg.fits")
    otpt = f + "-" + l
    line_1 = "%s: %s %s\n" % (otpt, program, " ".join(input_list))
    line_2 = "\t%s %s -o %s\n\n" % (program, " ".join(input_list), otpt)
    entry = line_1 + line_2
    return entry


def write_makeflow(makeflow_task_list):
    """
    Write Makeflow
    From a list of makeflow tasks (already formatted), write entries to an output makeflow file.

    :param makeflow_task_list: List of makeflow entries (from spawn_makeflow_entry)
    :return: None (writes to output file)
    """
    fitsavg_loc = '/home/u25/ahaug/library/bin/fitsavg'
    mf_head = "FITSAVG=%s\n\n" % fitsavg_loc
    with open("average.mf", 'w') as makeflow:
        makeflow.write(mf_head)
        for task in makeflow_task_list:
            makeflow.write(task)


composition = analyze_sorted(argv[1])
makeflow_entries = []
for group in composition:
    if group["type"] == 'DARK':
        entry = spawn_makeflow_entry('$FITSAVG', group['contents'])
        makeflow_entries.append(entry)

write_makeflow(makeflow_entries)
log = generate_log(composition)

end = datetime.now()
duration = end - start
print "FITS Averaging Complete"
print "Total Execution Time (seconds): %d.%d" % (duration.seconds, duration.microseconds)
print ''.join(log).rstrip('\n')