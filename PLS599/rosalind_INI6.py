#Rosalind Python Village
#INI6 "Dictionaries"
#by Asher Baltzell, 2/9/15

#Create an empty dictionary to store words
s_dict = {}

#Open input file as inpt
with open('ini6.txt', 'r') as inpt:
	#Save inpt string as s, then split into list of words
	s = inpt.read()
	s_ls =  s.split()

#Iterate through list of words
for item in s_ls:
	#If word is already in dictionary, increase count by 1
	if item in s_dict:
		s_dict[item] += 1
	#If not already in dictionary, add and set count to 1
	else:
		s_dict[item] = 1

#Iterate through items in dictionary
for key, value in s_dict.iteritems():
	#Print key and value to terminal
	print("%s %i") % (key, value)	
