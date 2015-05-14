__author__ = 'asherkhb'
# treejoiner.py
# Combines multiple, single-tree newick files into a single, multi-tree newick file.
#
# User must modify "User Assigned Variables" to represent their specific files and locations.

# User Assigned Variables
outputfile = "./duptree/bootstraps.newick"
tree_number = 100
base_name = "./duptree/species_bootstrap"

with open(outputfile, 'w') as otpt:
    for i in range(1, tree_number+1):
        filename = base_name + "_%i.newick" % i
        with open(filename, 'r') as treefile:
            tree = treefile.readlines()
            otpt.write(tree[3])