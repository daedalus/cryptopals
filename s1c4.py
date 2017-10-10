import fileinput

def f(f1,n1):
	tmp = ""
	for i in range(0,len(f1)):
		tmp += chr(ord(f1[i]) ^ n1)
	return tmp

c = 0
for line in fileinput.input():
	c+=1
	i1 = line.rstrip().decode('hex')
	for i in range(0,255):
		print c,i,f(i1,i)

#answer 171 53
