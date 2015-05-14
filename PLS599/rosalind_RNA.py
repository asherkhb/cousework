#Rosalind Bioinformatics Stronghold
#DNA "Transcribing DNA into RNA
#by Asher Baltzell, 2/10/15

#Opens file containing DNA string
with open('rna.txt', 'r') as inpt:
	#Sets variable "dna" as string from input file
	dna = inpt.read()

#Converts DNA to RNA. All "T" replaced with "U". New line stripped so no blank line on terminal.
rna = dna.replace("T", "U").strip('\n')

#Print resulting RNA string to terminal
print rna
