#Rosalind Python Village
#INI2 "Variables and Some Arithmetic"
#by Asher Baltzell, 2/8/14

#Open input file
with open('ini2.txt', 'r') as inpt:
	#Read input file to string i
	i = inpt.read()
	#Split i into list
	int_list = i.split()

#Assign triangle legs to a and b, set as integers	
a = int(int_list[0])
b = int(int_list[1])
#Calculate square of hypotenuse, set as c2
c2 = (a*a) + (b*b)

#Return solution to terminal
print(c2)
