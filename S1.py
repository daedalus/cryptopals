import sys
def hextobase64(h):
	return h.decode('hex').encode('base64').replace('\n','') 

def XOR(a,b):
	tmp =""
	if len(a) == len(b):
		for i in range(0,len(a)):
			tmp += chr(ord(a[i]) ^ ord(b[i]))
		return tmp
	else:
		raise Exeption("String Missmatch")


def singleByteXOR(a,b):
	tmp = ""
	for i in range(0,len(a)):
		tmp += chr(ord(a[i]) ^ b)
	return tmp

def repeatingXOR(ciphertext,key):
        tmp = ""
        for i in range(0,len(ciphertext)):
                tmp += chr(ord(ciphertext[i]) ^ ord(key[i % len(key)]))
        return tmp

def scoreChiSQ(str):
	expFreqsIncludingSpace = [0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442, 0.0197881, 0.0158610, 0.0492888, 0.0558094, 0.0009033, 0.0050529, 0.0331490, 0.0202124, 0.0564513, 0.0596302, 0.0137645, 0.0008606, 0.0497563, 0.0515760, 0.0729357, 0.0225134, 0.0082903, 0.0171272, 0.0013692, 0.0145984, 0.0007836, 0.1918182]
	str = str.lower()
	CHARS_CONSIDERED=27	
	charCounts = [0] * 27
	charFreqs = [0.0] *27
	totCount = 0;

	for c in list(str):
        	index = ord(c) - ord("A")
        	if(index>=0 and index<26):
            		charCounts[index]+=1
            		totCount+=1
        
        	if(c==' '):
            		charCounts[26]+=1
            		totCount+=1
	
    	if(totCount==0):
		totCount=1; #//avoid divide by zero

    	chiSquaredScore=0.0;

	for i in range(0,CHARS_CONSIDERED):
        	charFreqs[i]=float(charCounts[i])/float(totCount)
        	chiSquaredScore += (charFreqs[i] - expFreqsIncludingSpace[i])*(charFreqs[i]-expFreqsIncludingSpace[i])/(expFreqsIncludingSpace[i])
	return chiSquaredScore;     

wl = []
def loadDict():
	global wl
	fp = open('/usr/share/dict/american-english')
	for line in fp:
		wl.append(line.rstrip())
	fp.close()

loadDict()

def dictScore(msg):
	global wl
	#print "wl:",len(wl)

	score = 0
	msg = msg.split(" ")
	for word in msg:
		if word in wl:
			score += 1
	return score

def findSingleByteXOR(data):
	best = 0.0
	key = 0
	cand = []
	plaintext = ""
	for KEY in range(0,255):
		plaintext = singleByteXOR(data,KEY)
		score = scoreChiSQ(plaintext)
		if score >= best:
			best = score
			cand.append((plaintext,KEY))
	BEST = 0
	print "cand:",len(cand)
	for plaintext,key in cand:
		score = dictScore(plaintext)
		#print score
		if score > BEST:
			BEST = score
			PLAINTEXT = plaintext
			KEY = key
			#print "score:",score
						
	return KEY,BEST,PLAINTEXT

def hammingDistance(msg1,msg2):
	d = XOR(msg1,msg2)
	count = 0
	for i in range(0,len(d)):
		for j in range(0,8):
			count += ((ord(d[i]) & (1 << j)) >> j)
	return count

def findRepeatingXORSize(data):
	bestScore = 0.0
	bestScore = sys.float_info.max
	for KEYSIZE in range(2,40):
		a = data[:KEYSIZE]
		b = data[KEYSIZE:KEYSIZE*2]		
		score = hammingDistance(a,b) / float(KEYSIZE)
		if score < bestScore:
			res = KEYSIZE
			bestScore = score
	return res


def findRepatingXORKey(data):
	blocks = []
	KEYSIZE=findRepeatingXORSize(data)

	print "KEYSIZE:",KEYSIZE	

	for i in range(0,len(data),KEYSIZE):
		blocks.append(list(data[i:i+KEYSIZE]))
	
	transposed = [[""] * len(blocks)] * int(len(data)/KEYSIZE)

	for i in range(0,len(blocks)):
		for j in range(0,len(blocks[i])):
			transposed[j][i] = blocks[i][j]
	
	def getCol(index):
		tmp = ""
		for i in range(0,len(blocks)):
			tmp += transposed[index][i]
		return tmp
	
	keys = []
	for index in range(0,int(len(data)/KEYSIZE)):
		print "index:",index
		col = getCol(index)
		key,score,p = findSingleByteXOR(col)
		print (key,score,p.encode('hex'),col.encode('hex'))

	return keys
	

def readBase64Decode(fn):
	fp = open(fn)
	data = ""
	for line in fp:
		line = line.rstrip()
		data += line
	return data.decode('base64')

data = readBase64Decode(sys.argv[1])
#print findRepeatingXORSize(data)
d = findRepatingXORKey(data)
for key in d:
	print key
