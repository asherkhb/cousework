__author__ = 'senorrift'


def analyze_sorted(csv_file):
    with open(csv_file, 'r') as inpt:
        header = next(inpt)
        current_type = ''
        current_count = 0
        for line in inpt:
            content = line.split(',')
            vimtype = content[2]
            if vimtype != current_type:
                if current_type != '':
                    print "%s: %d" % (current_type, current_count)
                current_type = vimtype
                current_count = 1
            else:
                current_count += 1
        print "%s: %d" % (current_type, current_count)

analyze_sorted('output.csv')