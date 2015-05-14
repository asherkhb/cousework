#Rosalind Python Village
#INI5 "Working with Files": Working Solution
#by Asher Baltzell, 2/8/15

#Set Counter for Lines
counter = 0

#Open input file
with open('ini5.txt', 'r') as inpt:
	#Create and open output file
	with open('ini5_out.txt', 'w') as otpt:
		#Read through lines
		for line in inpt:
			counter += 1
			#If even numbered line, print to output
			if counter % 2 == 0:
				otpt.write(line)
