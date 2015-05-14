__author__ = 'asherkhb'
# auto_duptree.py
# Automatically executes DupTree repeatedly for generating bootstrap replicates of species trees.
# Coverage files generated with XXXSCRIPT!!
#
# User must modify "x" to represent their specific files.

from subprocess import call

# Number of bootstrap replicates desired.
run_number = 100

for i in range(1, run_number+1):
    # Modify "x" to represent specific files.
    x = 'duptree -i gene_bootstrap_%i.nwk -o ./duptree/species_bootstrap_%i.newick --oformat newick --nogenetree'\
        % (i, i)
    call(x, shell=True)