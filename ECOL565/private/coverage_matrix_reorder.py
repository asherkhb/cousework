__author__ = 'asherkhb'

from sys import argv
import cPickle as pickle

list = argv[1]
csv = argv[2]

csv_content = {}
head = ''

ordered_spp = pickle.load(open(list, 'rb'))

with open(csv, 'r') as inpt:
    for line in inpt:
        line_split = line.split(',')
        spp = line_split[0]
        if spp == 'Species':
            head = line
        else:
            csv_content[spp] = line

with open('_ordered_coverage_matrix.csv', 'w') as otpt:
    otpt.write(head)
    for spp in ordered_spp:
        otpt.write(csv_content[spp])