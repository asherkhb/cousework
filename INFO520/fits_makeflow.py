#!/usr/bin/env python

import argparse
from datetime import datetime
import multiprocessing as mp

__author__ = 'senorrift'
start = datetime.now()


def parse_img_csv(csv_file):
    """
    Parse FITS Header CSV
    From a sorted CSV of select FITS header information (generatd with fits_head_extract_*.py, then sorted by date)
    Generate a list of input/reference pairs.

    :param csv_file: sorted, FITS header CSV (i.e. from fits_head_extract_parallel.py, then sorted by date)
    :return: List of required tasks [{"input":<inputfile>, "reference":<referencefile>}, ...]
    """
    required_tasks = []

    current_reference = ''
    with open(csv_file, 'U') as inpt:
        for line in inpt:
            contents = line.split(",")
            filename = contents[0]
            vimtype = contents[2]
            if vimtype == 'DARK':
                current_reference = filename
            elif vimtype == 'SCIENCE':
                if current_reference != '':
                    required_tasks.append({"input": filename, "reference": current_reference})
                else:
                    print "ERROR [%s]: No reference identified."
            else:
                if vimtype == "IMAGETYPE":
                    pass
                else:
                    print "ERROR [%s]: Unrecognized image type."
    return required_tasks


def spawn_makeflow_entry(program, inputf, reference):
    """
    Spawn Makeflow Entry.
    From a program, input, and reference, generates a makeflow entry for that input.
    Currently designed to work with 'fitssub' (LINK).

    :param program: program that will be run (i.e. 'fitssub')
    :param inputf: input FITS file (usually with VIMTYPE='SCIENCE')
    :param reference: reference FITS file (usually with VIMTYPE='DARK')
    :return: makeflow entry (str)
    """
    otpt = inputf.replace('.fits', '_sub.fits')
    line_1 = "%s: %s %s %s\n" % (otpt, program, inputf, reference)
    line_2 = "\t%s -i %s -r %s -o %s\n\n" % (program, inputf, reference, otpt)
    entry = line_1 + line_2
    return entry


def write_makeflow(makeflow_task_list):
    """
    Write Makeflow
    From a list of makeflow tasks (already formatted), write entries to an output makeflow file.

    :param makeflow_task_list: List of makeflow entries (from spawn_makeflow_entry)
    :return: None (writes to output file)
    """
    mf_head = "FITSSUB=%s\n" % fitssub_loc
    with open(output_file, 'w') as makeflow:
        makeflow.write(mf_head)
        for task in makeflow_task_list:
            makeflow.write(task)


# # ----- Parse arguments. ----- # #
# Setup parser.
parser = argparse.ArgumentParser(description="FITS Image Processing Makeflow Generator",
                                 epilog="For more help, visit XXX")
# Input CSV (-i)
parser.add_argument('-i',
                    type=str,
                    default="output.csv",
                    help="input CSV (must be sorted)")
# Output Makeflow file (-o)
parser.add_argument('-o',
                    type=str,
                    default="makeflow.mf",
                    help="output Makeflow filename")
# TODO: Add ability to specify a path for images.
parser.add_argument('-p',
                    type=str,
                    # default="./",
                    help="path to images")
# Use Program (-u)
parser.add_argument('-u',
                    type=str,
                    default="./fitssub",
                    help="use program (tip: use absolute path to program)")
# Parallelize (-P)
parser.add_argument("-P",
                    action="store_true",
                    help="use parallelized processing")
# Parse Arguments
args = parser.parse_args()

# # ----- Assign input/output/program location. ----- # #
input_file = args.i
output_file = args.o
fitssub_loc = args.u

# # ----- Parse input CSV into jobs list ----- # #
jobs = parse_img_csv(input_file)

# # ----- Create list of Makeflow Tasks ----- # #
if args.P:
    # Parallel Processing (slower with few entries)
    task_pool = mp.Pool()
    makeflow_tasks = [task_pool.apply(spawn_makeflow_entry,
                                      args=("$FITSSUB", job["input"], job["reference"],)) for job in jobs]
else:
    # Serial Processing (faster with few entries)
    makeflow_tasks = []
    for job in jobs:
        makeflow_tasks.append(spawn_makeflow_entry("$FITSSUB", job["input"], job["reference"]))


# # ----- Execute Main Script ----- # #
write_makeflow(makeflow_tasks)
end = datetime.now()
duration = end - start
print "FITS Makeflow Generation Complete"
print "Total Execution Time (seconds): %d.%d" % (duration.seconds, duration.microseconds)
