__author__ = 'asherkhb'

import cPickle as pickle

high_coverage = '(+)'
low_coverage = '(-)'

species = pickle.load(open('threshold5_threshold2_subtr_species.p', 'rb'))

with open('threshold5_threshold2_subtree.nexml', 'r') as inpt, open('threshold5_threshold2_subtree_appended.nexml', 'w') as otpt:
    content = inpt.read()
    for spp in species:
        new_name = spp + '...................................................................'
        content = content.replace(spp, new_name)
        #content = content.replace(low_coverage, '')
    otpt.write(content)