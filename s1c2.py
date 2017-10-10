i1 = '1c0111001f010100061a024b53535009181c'
i2 = '686974207468652062756c6c277320657965'
o1 = '746865206b696420646f6e277420706c6179'

i1 = i1.decode('hex')
i2 = i2.decode('hex')

def f(f1,f2):
	tmp =""
	for i in range(0,len(i1)):
		tmp += chr(ord(i1[i]) ^ ord(i2[i]))
	return tmp

print f(i1,i2).encode('hex') == o1
