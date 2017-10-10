i1 = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
i1 = i1.decode('hex')

def f(f1,n1):
	tmp = ""
	for i in range(0,len(f1)):
		tmp += chr(ord(f1[i]) ^ n1)
	return tmp

for i in range(0,255):
	print i,f(i1,i)

#answer 88
