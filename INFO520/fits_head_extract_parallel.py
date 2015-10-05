#!/usr/bin/env python

import argparse
from datetime import datetime
from os import listdir, path
import multiprocessing as mp

__author__ = 'asherkhb'
start = datetime.now()


def extract_metadata(fits_file):
    f = pyfits.open(fits_file)
    filename = path.basename(fits_file)
    head = f[0].header
    # print repr(head)  # Print entire header
    obsdate = head['DATE-OBS']
    vimtype = head['VIMTYPE']
    vshutter = head['VSHUTTER']
    aoloopst = head['AOLOOPST']

    metadata = {"filename": filename,
                "obsdate": obsdate,
                "vimtype": vimtype,
                "vshutter": vshutter,
                "aoloopst": aoloopst}

    f.close()
    return metadata


def print_summary(img_total, science_count, dark_count, open_count, shut_count, error_count):
    print "Dataset Composition\n" \
      "> TOTAL Images: %d\n" \
      "> SCIENCE Images: %d\n" \
      "> DARK Images: %d\n" \
      "> OPEN Shutter: %s\n" \
      "> CLOSED Shutter: %d\n" \
      "> ERRORS: %d" % (img_total, science_count, dark_count, open_count, shut_count, error_count)


# Future options:
#    Inputs
#      -u <url to images>
#    Checkpointing
#      -s <filename> --> save checkpointing to filename
#      -r <filename> --> resume from checkpointing file

# Parse arguments
parser = argparse.ArgumentParser(description="FITS Image Processing",
                                 epilog="For more help, visit XXX")
parser.add_argument('-p',
                    type=str,
                    default="./",
                    help="path to images")
parser.add_argument('-o',
                    type=str,
                    default="output.csv",
                    help="output metadata CSV filename")
parser.add_argument("-H",
                    action="store_true",
                    help="use HPC mode")
parser.add_argument("-V",
                    action="store_true",
                    help="validate entries before producing output")
args = parser.parse_args()

# Import appropriate FITS library.
if args.H:
    from astropy.io import fits as pyfits
else:
    import pyfits

# Assign input/output.
img_directory = args.p
output_file = args.o

# From path to image directory, find all *.fits files and save in file_queue, and save all other files in alt_files.
file_queue = []
alt_files = []
for f in listdir(img_directory):
    if f.endswith(".fits"):
        file_queue.append(img_directory + '/' + f)
    else:
        alt_files.append(img_directory + '/' + f)

# Summary variables.
science_count = 0
dark_count = 0
open_count = 0
shut_count = 0
error_count = 0

# Analyze each file (paralleled).
meta_pool = mp.Pool()
meta_list = meta_pool.map(extract_metadata, file_queue)

csv_entries = []
for meta in meta_list:
    error = 0
    # Populate summary variables.
    if meta["vimtype"] == 'SCIENCE':
        science_count += 1
    elif meta["vimtype"] == "DARK":
        dark_count += 1
    else:
        error = 1
        error_count += 1
        print "ERROR [%s]: Unrecognized Image Type (%s)" % (meta["filename"], meta["vimtype"])

    if meta["vshutter"] == 'OPEN':
        open_count += 1
    elif meta["vshutter"] == 'SHUT':
        shut_count += 1
    else:
        error = 1
        error_count += 1
        print "ERROR [%s]: Unrecognized Shutter State (%s)" % (meta["filename"], meta["shutter"])

    if meta["vimtype"] == 'SCIENCE' and meta["vshutter"] == 'SHUT':
        error = 1
        error_count += 1
        print "ERROR [%s]: Image Type/Shutter State Conflict (%s, %s)" % (meta["filename"],
                                                                          meta['vimtype'],
                                                                          meta['vshutter'])
    elif meta["vimtype"] == 'DARK' and meta["vshutter"] == 'OPEN':
        error = 1
        error_count += 1
        print "ERROR [%s]: Image Type/Shutter State Conflict (%s, %s)" % (meta["filename"],
                                                                          meta['vimtype'],
                                                                          meta['vshutter'])

    if meta["vimtype"] == 'SCIENCE' and meta["aoloopst"] == 'OPEN':
        error = 1
        error_count += 1
        print "ERROR [%s]: AOLOOPST Open for Science Image (%s, %s)" % (meta["filename"],
                                                                        meta['vimtype'],
                                                                        meta['vshutter'])

    # Compile Entry and append to entries list
    entry = "%s,%s,%s,%s,%s\n" % (meta["filename"],
                                  meta["obsdate"],
                                  meta["vimtype"],
                                  meta["vshutter"],
                                  meta["aoloopst"])
    if args.V:
        if error:
            pass
        else:
            csv_entries.append(entry)
    else:
        csv_entries.append(entry)

# Generate output CSV.
csv_header = "FILENAME,DATETIME,IMAGETYPE,SHUTTER,AOLOOPST\n"
with open(output_file, 'w') as otpt:
    otpt.write(csv_header)
    for entry in csv_entries:
        otpt.write(entry)

# Calculate runtime.
end = datetime.now()
duration = end - start

# Write summary to stdout.
print "FITS-HEAD-EXTRACT is completed!"
print "Total Execution Time (seconds): %d.%d" % (duration.seconds, duration.microseconds)
print_summary(len(file_queue), science_count, dark_count, open_count, shut_count, error_count)
if not args.V and error_count > 0:
    print("WARNING: Output contains files with known errors. "
          "To produce output with these error files omitted, use the -V flag")
