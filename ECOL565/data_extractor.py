__author__ = 'asherkhb'

from re import search

master_msa = 'legumes.phy'
datasets = ['40species_ordered.txt', '80species_ordered.txt']

for dataset in datasets:
    species_list = []
    saved_content = []
    outputfile = dataset.strip('_ordered.txt') + '.phy'

    with open(dataset, 'r') as species:
        for line in species:
            cleanline = line.strip('\n').strip('\r').strip(' ')
            species_list.append(cleanline)

    with open(master_msa, 'r') as msa, open(outputfile, 'w') as otpt:
        firstline = True
        for line in msa:
            if firstline:
                linesplit = line.split(' ')
                msa_species = linesplit[0]
                new_species = str(len(species_list))
                msa_seqlen = linesplit[1].strip('\n')
                header = new_species + ' ' + msa_seqlen + '\n'
                otpt.write(header)
                firstline = False

            else:
                linesplit = line.split(' ')
                linespp = linesplit[0]
                if linespp in species_list:
                    otpt.write(line)
                else:
                    pass



