#!/usr/bin/env python
# Author Dario Clavijo 2017

import sys
import itertools
from Crypto.Cipher import AES
unpad = lambda s: s[:-ord(s[-1:])]

def hextobase64(h):
	return h.decode('hex').encode('base64').replace('\n','')

def XOR(a,b):
	if len(a) == len(b):
		return "".join(chr(ord(a[i]) ^ ord(b[i])) for i in range(0,len(a)))
	else:
		raise Exeption("String size Missmatch")

def singleByteXOR(a,b):
	return "".join(chr(ord(a[i]) ^ b) for i in range(0,len(a)))

def repeatingXOR(ciphertext,key):
	return "".join(
		chr(ord(ciphertext[i]) ^ ord(key[i % len(key)]))
		for i in range(0, len(ciphertext))
	)

def englishScore(string):
	freq = dict()
	freq['a']=834
	freq['b']=154
	freq['c']=273
	freq['d']=414
	freq['e']=1260
	freq['f']=203
	freq['g']=192
	freq['h']=611
	freq['i']=671
	freq['j']=23
	freq['k']=87
	freq['l']=424
	freq['m']=253
	freq['n']=680
	freq['o']=770
	freq['p']=166
	freq['q']=9
	freq['r']=568
	freq['s']=611
	freq['t']=937
	freq['u']=285
	freq['v']=106
	freq['w']=234
	freq['x']=20
	freq['y']=204
	freq['z']=6
	freq[' ']=2320
	return sum(freq[c] for c in string.lower() if c in freq)

def findSingleByteXOR(data):
	BEST = 0
	KEY = 0
	PLAINTEXT = ""
	for key in range(0,255):
		plaintext = singleByteXOR(data,key)
		score = englishScore(plaintext)
		if score > BEST:
			BEST = score
			KEY = key
			PLAINTEXT = plaintext
	return KEY,BEST,PLAINTEXT

def hammingDistance(msg1,msg2):
	d = XOR(msg1,msg2)
	return sum(
		((ord(d[i]) & (1 << j)) >> j)
		for i, j in itertools.product(range(0, len(d)), range(0, 8))
	)

def findXORBLOCKSize(n,data):
	BESTSCORE = sys.float_info.max
	KEYSIZE=0
	for keysize in range(1,64):
		a = data[:keysize*n]
		b = data[keysize*n:keysize*n*2]
		score = hammingDistance(a,b)
		score /= float(keysize)
		if score < BESTSCORE:
			KEYSIZE = keysize
			BESTSCORE = score
	return KEYSIZE,BESTSCORE

def findRepatingXORKey(data):
	best = 0
	KEY = ""
	blocks = []
	keysize,best=findXORBLOCKSize(1,data)

	blocksize=len(data)/keysize
	blocks = [""] * keysize
	for i in range(0,len(data)):
		blocks[i % keysize] += data[i]
	key = ""
	for block in blocks:
		k,s,t = findSingleByteXOR(block)
		key += chr(k)
	score = englishScore(key)
	if score > best:
		best = score
		KEY = key
	return KEY

def readBase64Decode(fn):
	fp = open(fn)
	data = ""
	for line in fp:
		line = line.rstrip()
		data += line
	return data.decode('base64')

def decryptECB(enc,key):
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.decrypt(enc)

def detectECB(data):
	distances = []
	blocks = [data[i:i+16] for i in range(0,len(data),16)]
	for i in range(0,len(blocks)):
		distances.extend(
			(i, j, hammingDistance(blocks[i], blocks[j]))
			for j in range(0, len(blocks))
			if i != j
		)
	return sum(1 for distance in distances if distance[2] == 0)

def test3():
	print "S1C3"
	print findSingleByteXOR("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".decode('hex'))

def test4():
	print "S1C4"
	i = 0
	BEST = 0
	PLAINTEXT =""
	fp = open('4.txt')
	for line in fp:
		i+=1
		line = line.rstrip()
		K,B,P = findSingleByteXOR(line.decode('hex'))
		if B > BEST:
			BEST = B
			KEY = K
			PLAINTEXT=P
	print BEST,KEY,PLAINTEXT

def crackRepeatingXOR(fn):
	data = readBase64Decode(fn)
	KEY = findRepatingXORKey(data)
	print "KEY:[", KEY,"]"
	print "DATA:\n",repeatingXOR(data, KEY)

def test6():
	print "S1C6"
	crackRepeatingXOR('6.txt')

def test7():
	print "S1C7"
	key = "YELLOW SUBMARINE"
	enc = open('7.txt').read().replace('\n','').decode('base64')
	print decryptECB(enc,key)

def test8():
	print "S1C8"
	fp = open('8.txt')
	for line in fp:
		data = line.replace('\n','').decode('hex')
		if detectECB(data) > 0:
			print data.encode('hex')


def tests():
	test3()
	test4()
	test6()
	test7()
	test8()

tests()
