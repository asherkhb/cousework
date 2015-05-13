__author__ = 'asherkhb'

from sys import argv
import cPickle as pickle

input_file = argv[1]
appending = argv[2]

def nexus_appender(input_file, appending):

    output_file = input_file.rstrip('.nexus').rstrip('.nex') + "_appended.nexus"
    with open(input_file, 'r') as inpt, open(output_file, 'w') as otpt:
        labels = False
        trees = False
        spp = []

        for line in enumerate(inpt):
            line_count = line[0]
            line_unaltered = line[1]
            line_contents = line_unaltered.strip('\n').strip(' ')

            if line_contents == 'TAXLABELS':
                labels = True
                otpt.write(line_unaltered)
                continue

            elif line_contents == ';':
                labels = False
                otpt.write(line_unaltered)
                continue

            elif line_contents == "BEGIN TREES;":
                trees = True
                otpt.write(line_unaltered)
                continue

            elif line_contents == "END;":
                trees = False
                otpt.write(line_unaltered)
                continue

            else:
                if labels:
                    appendee = line_unaltered.strip('\n').rstrip(' ')
                    new_line = appendee + appending + '\n'
                    otpt.write(new_line)
                    spp.append(line_contents)
                else:
                    if trees:
                        if line_unaltered != '\n':
                            new_line = line_unaltered
                            for sp in spp:
                                appended_name = sp + appending
                                new_line.replace(sp, appended_name)
                            otpt.write(new_line)
                        else:
                            otpt.write(line_unaltered)
                    else:
                        otpt.write(line_unaltered)

    pickle.dump(spp, open('species_ordered.p', 'wb'))

    return spp

nexus_appender(input_file, appending)