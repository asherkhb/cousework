"""
	fastq2fasta.py
	A Simple FASTQ to FASTA Conversion Script
	by Asher Baltzell - 1/26/15
	
	Help: -h
	Input: -i 'filename'

"""

import sys, getopt, os
from Bio import SeqIO

def main(argv):
	inputfile = ''
	outputfile = ''
	
	try:
		opts, args = getopt.getopt(argv, 'hi:')
	except getopt.GetoptError:
		print "Incorrect syntax: Use '-h' for help."
		with open('fastq2fasta_error-log.txt', 'w') as error:
			error.write("Syntax Error\n")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('Use Syntax: fastq2fasta.py -i <inputfile>')
			sys.exit()
		elif opt == '-i':
			inputfile = arg
			filename, extension = os.path.splitext(arg)
			outputfile = '%s.fasta' % (filename)			

	if inputfile == '':
		print("Incorrect syntax: Use '-h' for help.")
		with open('fastq2fasta_error-log.txt', 'w') as error:
			error.write("Syntax Error\n")
		sys.exit(2)

	with open(inputfile, 'r') as inpt:
		with open(outputfile, 'w') as otpt:
			SeqIO.convert(inputfile, "fastq", outputfile, "fasta")
			otpt.write(outputfile)
			print('Your FASTQ has been converted. See %s') % (outputfile)

if __name__ == '__main__':
	main(sys.argv[1:])