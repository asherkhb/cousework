__author__ = 'asherkhb'

import random
random.seed()


max_sets = 100
otptfilebase = 'gene_bootstrap'
ordered_gene_list = ['18s', '26s', 'atpB', 'ITS', 'matK', 'rbcL', 'trnLtrnF']
inputs = {"18s":"18s_bootstrap.nwk",
          "26s":"26s_bootstrap.nwk",
          "atpB":"atpB_bootstrap.nwk",
          "ITS":"ITS_bootstrap.nwk",
          "matK":"matK_bootstrap.nwk",
          "rbcL":"rbcL_bootstrap.nwk",
          "trnLtrnF":"trnLtrnF_bootstrap.nwk"}

trees = {}
used_vals = {}

for gene in inputs:
    trees[gene] = []
    used_vals[gene] = []
    with open(inputs[gene], 'U') as inpt:
        for line in inpt:
            trees[gene].append(line)

for i in range(0, max_sets):
    output_file = "./_bootstraps/%s_%i.nwk" % (otptfilebase, i + 1)
    with open(output_file, 'w') as otpt:
        contents = {}
        for gene in trees:
            found_tree = False
            while not found_tree:
                ran = random.randint(0, max_sets - 1) ##### Generate random number 0 - max trees
                if ran not in used_vals[gene]:
                    contents[gene] = trees[gene][ran]
                    used_vals[gene].append(ran)
                    found_tree = True
                else:
                    pass
        for gene in ordered_gene_list:
            file_entry = '[%s]\n[&R]%s' % (gene, contents[gene])
            otpt.write(file_entry)


