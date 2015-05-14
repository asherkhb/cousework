#Rosalind Python Village
#INI4 "Conditions and Loops"
#by Asher Baltzell, 2/9/15

#Set total variable at 0 to start
total = 0

#Open input file
with open('ini4.txt', 'r') as inpt:
	#Read and parse input file into two integers, a & b
	i = inpt.read()
	i_ls = i.split()
	a = int(i_ls[0])
	b = int(i_ls[1])

#Iterate through each number in the range a - b (inclusively)
for x in range(a, b+1):
	#Add odd numbers to total
	if x % 2 != 0:
		total += x

#Print total sum of all odd numbers in range a - b (inc.) to terminal
print(total) 
