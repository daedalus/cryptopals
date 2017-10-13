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

def oracleECBCBC(message):
	BS=AES.block_size
	key = Random.new().read(BS)
	g = Random.new().read(10)
	r = random.randrange(2)
	message = (g + message + g).zfill(96)
	if r == 1:
		data = encryptECB(message,key)
	else:
		IV = Random.new().read(BS)
		data = encryptCBC(message,key,IV)	
	return data

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
	print decryptCBC(data,'YELLOW SUBMARINE',IV)


def test3():
	for i in range(0,10):
		c = oracleECBCBC('THIS IS A VERY IMPORTANT MESSAGE FOR DECRYPT')
		ecb = detectECB(c)
		if ecb > 0:
			print "ECB",c.encode('hex')
		else:
			print "CBC",c.encode('hex')

#test1()
#test2()
test3()
