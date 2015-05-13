__author__ = 'asherkhb'

from sys import argv

missing_log = argv[1]
msa = argv[2]
outputfile = '.' + msa.strip('.phy') + '_thinned.phy'

missing_spp = []
missing_spp_number = 0
msa_contents = []

with open(missing_log, 'r') as missing_inpt:
    for line in missing_inpt:
        line_split = line.split(' ')
        missing_sp = line_split[2]
        try:
            missing_spp_number = int(missing_sp)
        except ValueError:
            missing_spp.append(missing_sp)

with open(msa, 'r') as msa_inpt:
    firstline = True
    for line in msa_inpt:
        line_split = line.split(' ')
        if firstline:
            total_spp = int(line_split[0])
            seq_length = int(line_split[1])
            new_spp = total_spp - missing_spp_number
            new_first_line = "%d %d\n" % (new_spp, seq_length)
            msa_contents.append(new_first_line)
            firstline = False
        else:
            sp = line_split[0]
            if sp not in missing_spp:
                msa_contents.append(line)
            else:
                pass

with open(outputfile, 'w') as otpt:
    for entry in msa_contents:
        otpt.write(entry)