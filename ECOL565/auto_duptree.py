__author__ = 'asherkhb'

from subprocess import call

#duptree -i 40sp_trees_rooted.nwk -o duptree_speciestree_40sp_rooted.nexus --oformat nexus --nogenetree

run_number = 100

for i in range(1, run_number+1):
    x = 'duptree -i gene_bootstrap_%i.nwk -o ./duptree/species_bootstrap_%i.newick --oformat newick --nogenetree'\
        % (i, i)
    call(x, shell=True)