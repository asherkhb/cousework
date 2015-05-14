#Rosalind Bioinformatics Stronghold
#DNA "Counting DNA Nucleotides"
#by Asher Baltzell, 2/9/15

#Set counters for nucleotides bases
a = 0
c = 0
g = 0
t = 0

#Open input sequence file, save as variable seq
with open('dna.txt', 'r') as inpt:
	seq = inpt.read()

#Obtain length of sequence
seq_len = len(seq)

#Iterate through sequence
for i in range(0, seq_len):
	#Increase base counters by 1 for each occurance
	if seq[i] == "A":
		a += 1
	elif seq[i] == "C":
		c += 1
	elif seq[i] == "G":
		g += 1
	elif seq[i] == "T":
		t += 1

#Print results to terminal
print("%i %i %i %i") % (a, c, g, t)
