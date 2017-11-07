#!/usr/bin/python3

import string

import numpy as np

start = input("Start position:")
start = start.upper()

mode = input("Mode: (D)ecrypt/(E)ncrypt:")
inpt = input("Enter text:")
if not mode.upper() in ["D", "E"]:
	mink = int(input("Enter minimum key length:"))
	maxk = int(input("Enter maximum key length:"))+1
	for l in range(mink, maxk):
		divd = [inpt[i:i+l] for i in range(0, len(inpt)-l+1, 1)]
		print(l)
		print("\n".join([" ".join(a) for a in divd]))
		
	exit()
		
	


inpt = inpt.upper()

key = input("Enter key for creating Vigener's table:")

stdalphabet = string.ascii_uppercase
alphabet = ""

for i in key:
	if not i in alphabet:
		alphabet+=i.upper()
for i in stdalphabet:
	if not i in alphabet:
		alphabet+=i

print(alphabet)
print(stdalphabet)

start_id = alphabet.find(start)


table = [[alphabet[(x+(26-y+start_id))%len(alphabet)] for x in range(len(alphabet))] for y in range(len(alphabet))]




print("\n".join([" ".join(a) for a in table]))

a = ""
for i in table:
	a += i[0]

key2 = a
#key2 = input("Enter key:")

key2 = key2.upper()
key3 = ""

for i in key2:
	if not i in key3:
		key3+=i

key2 = key3

print ("Key: ", key2)



outpt = ""

print("")
#print(alphabet)


print("")

if mode.upper() == "E":
	for num,i in enumerate(inpt):
		col = stdalphabet.index(i)
		row = num%len(key2)
		outpt+=table[row][col]
elif mode.upper() == "D":
	for num, i in enumerate(inpt):
		row = num%len(key2)
		outpt += stdalphabet[table[row].index(i)]
		

print(outpt)
