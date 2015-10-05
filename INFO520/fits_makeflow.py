import argparse
from datetime import datetime
import multiprocessing as mp

__author__ = 'senorrift'
start = datetime.now()


def spawn_makeflow_entry(program, input, reference):
    """

    :param program:
    :param input:
    :param reference:
    :return:
    """
    otpt = input.replace('.fits', '_sub.fits')
    line_1 = "%s: %s %s %s\n" % (otpt, program, input, reference)
    line_2 = "\t%s -i %s -r %s -o %s\n\n" % (program, input, reference, otpt)
    entry = line_1 + line_2
    return entry


def parse_img_csv(csv_file):
    """

    :param csv_file:
    :return:
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


def write_makeflow(makeflow_task_list):
    with open(output_file, 'w') as makeflow:
        for task in makeflow_task_list:
            makeflow.write(task)


# # ----- Parse arguments. ----- # #
parser = argparse.ArgumentParser(description="FITS Image Processing Makeflow Generator",
                                 epilog="For more help, visit XXX")
parser.add_argument('-i',
                    type=str,
                    default="output.csv",
                    help="input CSV (must be sorted)")
parser.add_argument('-o',
                    type=str,
                    default="makeflow.mf",
                    help="output Makeflow filename")
parser.add_argument("-P",
                    action="store_true",
                    help="use parallelized processing")
args = parser.parse_args()


# # ----- Assign input/output. ----- # #
input_file = args.i
output_file = args.o

# # ----- Parse input CSV into jobs list ----- # #
jobs = parse_img_csv(input_file)

# # ----- Create list of Makeflow Tasks ----- # #
if args.P:
    # Parallel Processing (currently slower @ 5 entries)
    task_pool = mp.Pool()
    makeflow_tasks = [task_pool.apply(spawn_makeflow_entry,
                                      args=("fitssub", job["input"], job["reference"],)) for job in jobs]
else:
    # Serial Processing (currently faster @ 5 entries)
    makeflow_tasks = []
    for job in jobs:
        makeflow_tasks.append(spawn_makeflow_entry("fitssub", job["input"], job["reference"]))


# # ----- Execute Main Script ----- # #
write_makeflow(makeflow_tasks)
end = datetime.now()
duration = end - start
print "FITS Makeflow Generation Complete"
print "Total Execution Time (seconds): %d.%d" % (duration.seconds, duration.microseconds)