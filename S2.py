#!/usr/bin/env python
# Autor Dario Clavijo 2017

pad = lambda s,n: s + chr(n- len(s)) * (n-len(s))
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def test1():
	u = ("Dario Clavijo")
	print u.encode('hex')
	p = pad(u,20)
	print p.encode('hex')
	u = unpad(p)
	print u.encode('hex')

test1()
