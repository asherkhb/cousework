#Rosalind Python Village
#INI3 "Strings and Lists"
#by Asher Baltzell, 2/9/15

#Open input file
with open('ini3.txt', 'r') as inpt:
	#Save first line (string) as s
	s = inpt.readline()
	#Save second line (indicies) as i
	i = inpt.readline()
	#Split i into list i_ls
	i_ls = i.split()

#Set indicies a, b, c, d
a = int(i_ls[0])
b = int(i_ls[1])
c = int(i_ls[2])
d = int(i_ls[3])

#Split string into slice a - b, then c - d (inclusively)
split_1 = s[a:b+1]
split_2 = s[c:d+1]

#Return result to terminal
print("%s %s") % (split_1, split_2)
