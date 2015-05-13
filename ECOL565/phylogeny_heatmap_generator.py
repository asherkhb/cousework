__author__ = 'asherkhb'

import cPickle as pickle

genes = ['18s', '26s', 'atpB', 'ITS', 'matK', 'rbcL', 'trnLtrnF']
msa = '80species.phy'
phylogeny = 'threshold5_threshold2_subtree.nexus'

def ordered_pickle_generator(input_NEXUS_file):

    output_file = input_NEXUS_file.rstrip('.nexus').rstrip('.nex') + "_species.p"

    with open(input_NEXUS_file, 'r') as inpt:
        labels = False
        trees = False
        spp = []

        for line in inpt:
            line_contents = line.strip('\n').strip(' ')

            if line_contents == 'TAXLABELS':
                labels = True
                continue

            elif line_contents == ';':
                labels = False
                continue

            elif line_contents == "BEGIN TREES;":
                trees = True
                continue

            elif line_contents == "END;":
                trees = False
                continue

            else:
                if labels:
                    if line != '\n':
                        spp.append(line_contents)
                    else:
                        pass
                else:
                    if trees:
                        pass    # Pulling list from a tree can go here
                    else:
                        pass

        pickle.dump(spp, open(output_file, 'wb'))

    return output_file


def coverage_summary_generator(master_file, gene_list):
    header = 'Species,' + ','.join(genes) + '\n'
    species = []
    gene_coverage = {}

    with open('_coverage_matrix.csv', 'w') as otpt:
        otpt.write(header)

        with open(msa, 'r') as inpt:
            firstline = True
            for line in inpt:
                if not firstline:
                    entry = line.split(' ')
                    entry = entry[0]
                    species.append(entry)
                else:
                    firstline = False

        for gene in gene_list:
            gene_coverage[gene] = {}
            gene_file = '80species_' + gene + '.phy_coverage.csv'
            with open(gene_file, 'r') as genefile:
                for line in genefile:
                    line_contents = line.split(',')
                    spp = line_contents[0]
                    coverage = line_contents[1].strip('\n')
                    gene_coverage[gene][spp] = coverage


        for spp in species:
            coverages = []
            for gene in gene_list:
                try:
                    coverages.append(gene_coverage[gene][spp])
                except KeyError:
                    coverages.append('0')
            entry = spp + ',' + ','.join(coverages) + '\n'
            otpt.write(entry)


def ordered_coverage_summary_generator(ordered_pickle_of_taxa, unordered_csv_summary):
    list = ordered_pickle_of_taxa
    csv = unordered_csv_summary

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


ordered_sp_list = ordered_pickle_generator(phylogeny)

coverage_summary_generator(msa, genes)

ordered_coverage_summary_generator(ordered_sp_list, '_coverage_matrix.csv')