__author__ = 'asherkhb'

#Output appending = <filename.phy>_coverage.csv

genes = ['18s', '26s', 'atpB', 'ITS', 'matK', 'rbcL', 'trnLtrnF']

for gene in genes:
    genefile = '80species_' + gene + '.phy'
    outfile = genefile + '_coverage.csv'

    with open(genefile, 'r') as inpt, open(outfile, 'w') as otpt:
        firstline = True
        seq_len = 0

        for line in inpt:

            line = line.strip('\n')
            linesplit = line.split(' ')

            if firstline:
                sp_num = linesplit[0]
                seq_len = int(linesplit[1])

                firstline = False

            else:
                basecount = 0
                absent = 0
                species = linesplit[0]
                sequence = linesplit[1]
                #print sequence
                for b in range(0, seq_len):
                    if sequence[b] == '-':
                        absent += 1
                    else:
                        basecount += 1
                coverage = float(basecount) / seq_len
                entry = '%s,%f\n' % (species, coverage)
                otpt.write(entry)