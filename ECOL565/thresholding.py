__author__ = 'asherkhb'
# thresholding.py
# Given a CSV summary of a phylogeny (with coverage values for each gene)
# Returns a list of species that have data for a minimum number of genes
#
# Usage thresholding.py <input_csv> <min_gene_threshold>
# Prints number of matches to terminal
# Generates input_threshold_<X>.csv

import csv

from sys import argv

inpt_file = argv[1]
threshold = int(argv[2])

spps = []
matches = {}

with open(inpt_file, 'r') as inpt:
    for line in inpt:
        reader = csv.reader(inpt, delimiter=',')
        for row in reader:
            gene_number = len(row) - 1
            spp = row[0]
            spps.append(spp)
            quality_score = 0
            for i in range(0, gene_number):
                if float(row[i + 1]) > 0.0:
                    quality_score += 1

            #if quality_score >= threshold:
            if quality_score == threshold:
                matches[spp] = quality_score

match_number = len(matches)
print match_number, 'MATCHES'

output_file = inpt_file.strip('.csv') + '_threshold_' + str(threshold) + '.csv'

"""
with open(output_file, 'w') as otpt:
    otpt.write('Species,Genes with Coverage\n')
    for species in spps:
        if species in matches:
            entry = '%s,%s\n' % (species, matches[species])
            otpt.write(entry)
"""