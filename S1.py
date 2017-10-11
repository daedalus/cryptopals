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

def scoreEnglish(message):
        letters = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	message = message.upper()

	def GFO(message):

        	listing = []
		frequency_analysis = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
        	for letter in message:
            		if letter.isalpha():
              			frequency_analysis[letter] += 1
        	def get_num (frequency_analysis):
            		return frequency_analysis[1]
        	unsorted_items = frequency_analysis.items()
        	sorted_items = sorted(unsorted_items, key = get_num)
        	descending = reversed(sorted_items)
        	descending = list(descending)
        	inorder = list()
        	for char in descending:
            		inorder.append(char)
		tmp = []
		for key in inorder:
            		if key[1] > 0:
                		tmp.append(key[0])
		return tmp
	FO = GFO(message)
	print FO
	score = 0
	for c in letters[:6]:
		if c in FO[:6]:
			score +=1
	for u in letters[-6:]:
		if u in FO[-6:]:
			score +=1
	return score

def findSingleByteXOR(data):
	c = 0
	for i in range(0,255):
		t = singleByteXOR(data,i)
		s = scoreEnglish(t)
		if s > best:
			best = s
			key = chr(i)
	return key  

print FA("Hello this is a well done test sir")
