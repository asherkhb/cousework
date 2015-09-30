from astropy.io import fits as pyfits
from os import listdir
from sys import argv

__author__ = 'asherkhb'

img_directory = argv[1]
output_file = 'otpt.csv'  # Will be from "-o"

# From path to image directory, find all *.fits files and save in file_queue, and save all other files in alt_files
file_queue = []
alt_files = []
for f in listdir(img_directory):
    if f.endswith(".fits"):
        file_queue.append(f)
    else:
        alt_files.append(f)

# Summary Variables
science_count = 0
dark_count = 0
open_count = 0
shut_count = 0
error_count = 0


# Analyze each file
csv_entries = []
for fits_file in file_queue:
    file_location = img_directory + '/' + fits_file
    current_file = pyfits.open(file_location)

    # Print HDUList info
    #current_file.info()

    # Create Header Object
    head = current_file[0].header

    # Print entire header
    #print repr(head)

    # Get Observation Date
    # DATE-OBS= '2014-11-04T05:35:16.481449' / Date of obs. YYYY-mm-ddTHH:MM:SS
    obsdate = head['DATE-OBS']
    obsdate = obsdate.replace('-', '').replace('T', '').replace(':', '').replace('.', '')
    #print obsdate

    # Get Image Type
    # VIMTYPE = 'SCIENCE '           / Image Type
    vimtype = head['VIMTYPE']
    #print vimtype

    # Get Shutter State
    # VSHUTTER= 'OPEN    '           / Status of VisAO Shutter
    vshutter = head['VSHUTTER']
    #print vshutter

    # Check for Completeness (Could be replaced with GREP)
    if vimtype == "SCIENCE":
        science_count += 1
        if vshutter == "OPEN":
            open_count += 1
            pass
        else:
            if vshutter == "SHUT":
                shut_count += 1
            error_count += 1
            print "ERROR1: Type/shutter mismatch [%s, %s] - %s" % (vimtype, vshutter, fits_file)

    elif vimtype == "DARK":
        dark_count += 1
        if vshutter == "SHUT":
            shut_count += 1
        else:
            if vshutter == "OPEN":
                open_count += 1
            error_count += 1
            print "ERROR2: Type/shutter mismatch [%s, %s] - %s" % (vimtype, vshutter, fits_file)

    else:
        if vshutter == "OPEN":
            open_count += 1
        elif vshutter == "SHUT":
            shut_count += 1
        error_count += 1
        print "ERROR3: Unknown vimtype [%s] - %s" % (vimtype, fits_file)


    # Compile Entry and append to entries list
    file_entry = "%s,%s,%s,%s\n" % (fits_file.rstrip(".fits"), obsdate, vimtype, vshutter)
    csv_entries.append(file_entry)

    # Close file
    current_file.close()

# Generate output CSV
csv_header = "FILENAME,DATETIME,IMAGETYPE,SHUTTER\n"
with open(output_file, 'w') as otpt:
    otpt.write(csv_header)
    for entry in csv_entries:
        otpt.write(entry)

# Write to stdout summary statistics.
print "FITS-HEAD-EXTRACT is completed!"
print "Dataset Composition\n" \
      "> TOTAL Images: %d\n" \
      "> SCIENCE Images: %d\n" \
      "> DARK Images: %d\n" \
      "> OPEN Shutter: %s\n" \
      "> CLOSED Shutter: %d\n" \
      "> ERRORS: %d" % (len(file_queue), science_count, dark_count, open_count, shut_count, error_count)
