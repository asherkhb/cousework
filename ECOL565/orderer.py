__author__ = 'asherkhb'

import cPickle as pickle

all_species = pickle.load(open('legume_species.p', 'rb'))
my_species = []

with open('80species_unordered_renamed.txt', 'r') as inpt:
    for line in inpt:
        line_thinned = line.strip('\n')
        my_species.append(line_thinned)

with open('80species_ordered.txt', 'w') as otpt:
    for spp in all_species:
        if spp in my_species:
            otpt.write(spp)
            otpt.write('\n')