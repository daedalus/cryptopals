#!/usr/bin/env python
# Autor Dario Clavijo 2017
from S1 import *
from Crypto.Cipher import AES
from base64 import *

pad = lambda s,n: s + chr(n- len(s)) * (n-len(s))
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encryptECB(enc,key):
        cipher = AES.new(key, AES.MODE_ECB)
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

#test1()
test2()
