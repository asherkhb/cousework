__author__ = 'asherkhb'

import csv

from sys import argv

input_nexus = argv[1]
output_nexus = input_nexus.strip('.nexus') + '_thresholded.nexus'
threshold_csv = argv[2]

threshold_spp = []

with open(threshold_csv, 'r') as threshold_inpt:
    for line in threshold_inpt:
        threshold_reader = csv.reader(threshold_inpt, delimiter=',')
        for row in threshold_reader:
            threshold_spp.append(row[0])

with open(input_nexus, 'r') as inpt, open(output_nexus, 'w') as otpt:
    content = inpt.read()
    for spp in threshold_spp:
        new_name = spp + '----------------------------------------------------------------------------------------'
        content = content.replace(spp, new_name)
    otpt.write(content)
