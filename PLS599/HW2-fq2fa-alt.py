
in_file = 'sample_1.fq'
out_file = 'sample_1-FASTA.fa'
line_counter = 0

with open(in_file, 'r') as inpt:
	with open (out_file, 'w') as otpt:
		for line in inpt:
			if line_counter == 4:
				line_counter = 0
		
			if line_counter <= 1:
				otpt.write(line.replace('@','>'))
				line_counter += 1
			else:
				line_counter += 1
