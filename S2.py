#!/usr/bin/env python
# Autor Dario Clavijo 2017
from S1 import *
from Crypto.Cipher import AES
from base64 import *
import random
from Crypto import Random

pad = lambda s,n: s + chr(n- (len(s)%n)) * (n-(len(s)%n))
unpad = lambda s: s[:-ord(s[-1:])]

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
        message = pad(g + message + g,16)
        if r == 1:
                return encryptECB(message,key)
        IV = Random.new().read(BS)
        return encryptCBC(message,key,IV)

def detectOracleMethod(encryptionOracle,message,key):
        c = encryptionOracle(message,key)
        return ("ECB", c.encode('hex')) if detectECB(c) else ("CBC", c.encode('hex'))

def findECBBLOCKSize(data):
        BESTSCORE = sys.float_info.max
        KEYSIZE=0
        for keysize in range(2,64):
                blocks = []
                for j in range(0,len(data),keysize):
			b = data[j:j+keysize]
			if len(b) == keysize:
                        	blocks.append(data[j:j+keysize])
                pairs = list(itertools.combinations(blocks, 2))
                scores = [hammingDistance(p[0], p[1])/float(keysize) for p in pairs]
		if len(scores) > 1:
                	s = float(sum(scores) / len(scores))
                	if s < BESTSCORE:
                	        BESTSCORE = s
                        	KEYSIZE = keysize
        return KEYSIZE,BESTSCORE

def detectOracleBLOCKSIZE(oracle,msg):
	return findECBBLOCKSize(oracle(msg))[0]

def getNextByte(oracle,blockSize,knownString):
        myString = "0" * (blockSize - (len(knownString) % blockSize) -1 )
        d = {}
        for i in range(0,256):
                candidate = oracle(myString+knownString+chr(i))
                l = len(myString) + len(knownString)+1
                d[candidate[:l]] = i
        target = oracle(myString)
        u = target[:l]
        return d.get(u, None)

def crackECBOracle(oracle,blockSize,knownBytes):
	while True:
		b = getNextByte(oracle,blockSize,knownBytes)
		if b is None:
			break
		knownBytes += chr(b)

	return knownBytes

def test9():
	print "C9-S2C1"
	u = ("Dario Clavijo")
	print u.encode('hex')
	p = pad(u,20)
	print p.encode('hex')
	u = unpad(p)
	print u.encode('hex')

def test10():
	IV = '\x00' * AES.block_size
	KEY = pad(b'YELLOW SUBMARINE',16)
	print KEY,KEY.encode('hex'),len(KEY),len(IV)
	data = b64decode(open('10.txt').read())
	print decryptCBC(data,KEY,IV)

def test11():
	for i in range(0,10):
		key = Random.new().read(16)
		msg = 'THIS IS A VERY IMPORTANT MESSAGE FOR DECRYPT'
		print detectOracleMethod(oracleECBCBC,msg,key)

def test12():
	key = Random.new().read(16)
	UNKNOWN = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

	def oracle(plaintext):
		# key is supposed to be internal to the oracle, we dont know it.
		plaintext = pad(plaintext+b64decode(UNKNOWN),16)
		c = encryptECB(plaintext,key)
		return c # ECB detected

	BLOCKSIZE = detectOracleBLOCKSIZE(oracle,"0"*32)

	print "BLOCKSIZE detected:",BLOCKSIZE

	if detectECB(oracle("1"*32)) == 0:
		print "ECB!"
		sys.exit(0)
	else:
		print "ECB MODE detected"

	print crackECBOracle(oracle,BLOCKSIZE,"")

def KVtoJSON(s):
        myjson = "{\n"
        for kv in s.split("&"):
                k,v = kv.split("=")
                myjson += f"{k}:{v}" + "\n"
        myjson += "}"
        return myjson

def JSONtoKV(s):
        s = replace("{\n",'').replace("}\n","")
        s = s.split("\n")
        kvs = []
        for l in s:
                k,v = l.split(':')
                kvs.append(f"{k}={v}")
        return "&".join(kvs)

#test9()
#test10()
#test11()
test12()
