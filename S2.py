#!/usr/bin/env python
# Autor Dario Clavijo 2017
from S1 import *
from Crypto.Cipher import AES
from base64 import *
import random
from Crypto import Random

pad = lambda s,n: s + chr(n- len(s)) * (n-len(s))
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encryptECB(enc,key):
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(enc)

def encryptCBC(enc,key,IV):
        cipher = AES.new(key, AES.MODE_CBC,IV)
        return cipher.encrypt(enc)
	
def decryptCBC(data,key,iv):
	l = len(iv)
	tmp = ""
	lastblock = iv
	for i in range(0,len(data),l):
		block = data[i:i+l]
		decrypted = decryptECB(block,key)
		plain = XOR(decrypted,lastblock)
		tmp += plain
		lastblock = block
	return tmp

def oracleECBCBC(message,key):
	BS = AES.block_size
	g = Random.new().read(10)
	r = random.randrange(2)
	message = (g + message + g).zfill(128)
	if r == 1:
		data = encryptECB(message,key)
	else:
		IV = Random.new().read(BS)
		data = encryptCBC(message,key,IV)	
	return data

def detectOracleMethod(encryptionOracle,message,key):
	c = encryptionOracle(message,key)
	if detectECB(c):
		return "ECB",c.encode('hex')
	return "CBC",c.encode('hex')

def test1():
	print "C9-S2C1"
	u = ("Dario Clavijo")
	print u.encode('hex')
	p = pad(u,20)
	print p.encode('hex')
	u = unpad(p)
	print u.encode('hex')

def test2():
	IV = '\x00' * AES.block_size 
	KEY = pad(b'YELLOW SUBMARINE',16)
	print KEY,KEY.encode('hex'),len(KEY),len(IV)
	data = b64decode(open('10.txt').read())
	print decryptCBC(data,KEY,IV)


def test3():
	for i in range(0,10):
		key = Random.new().read(16)
		msg = 'THIS IS A VERY IMPORTANT MESSAGE FOR DECRYPT'
		print detectOracleMethod(oracleECBCBC,msg,key) 

def test4():
	key = Random.new().read(16)
	UNKNOWN = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
	KNOWN = ""

		

	def oracle(msg,key):
		c = encryptECB(msg,key)
		return c # ECB detected

	if detectECB(oracle(UNKNOWN.zfill(224),key)) == 0:
		sys.exit(0)
	else:
		print "ECB MODE detected"

	def detectOracleBLOCKSIZE(oracle,msg,key):
		c = oracle(msg,key)
		B,s = findBLOCKSize(1,c)
		return B

	print "LEN UNKNOWN DATA:",len(UNKNOWN)
	BLOCKSIZE = detectOracleBLOCKSIZE(oracle,UNKNOWN.zfill(256),key)

	print "BLOCKSIZE detected:",BLOCKSIZE



	def findnNextByte(oracle,BLOCKSIZE,KNOWN):	
		#print len(UNKNOWN[0:BLOCKSIZE])
		target = oracle(UNKNOWN[0:BLOCKSIZE],key)
		#print target
		print "Target:",target.encode('hex')
		ISTR = UNKNOWN[0:BLOCKSIZE-1]
		for i in range(0,255):
			test = ISTR + chr(i)
			testc = oracle(test,key)
			if testc == target:
				return chr(i)
		return None

	while True:
		b = findnNextByte(oracle,BLOCKSIZE,UNKNOWN)
		KNOWN += b
		if b != None:
			break

	print KNOWN
		
	

#test1()
#test2()
#test3()
test4()

