# -*- coding: utf-8 -*-

from collections import Counter
import sys, argparse, re, pickle, math
import ngramProfiler
import ast

def main(corpus):
	try:
		with open(corpus, 'rb') as f:
<<<<<<< HEAD
			P1 = normalize(pickle.load(f))
			print(P1)
			# P1 = ast.literal_eval(s)
			file = open('database\\test_POStags', 'r')
			text = file.read()
			file.close
			P2 = normalize(ngramProfiler.main(text,3))
			print(P2)
			calcDiff(P1, P2)
	except IOError: 
		print('Cannot open '+corpus)
=======
			P1 = pickle.load(f)
			# print(P1)
			# P1 = pickle.load(f)
			# print(P1)
			# P1 = ast.literal_eval(s)
			file = open('database\\bla', 'r')
			text = file.read()
			file.close
			P2 = ngramProfiler.main(text,3)
			# P2 = ngramProfiler.main(text,3)
			# print(P2)
	except IOError: 
		print('Cannot open '+corpus)
	# calcDiffW(P1, P2)
	calcDiffUw(P1, P2)


def calcDiffW(P1,P2):
	D = 0.0
	P1l = Counter(list(P1))
	print(len(P1l))
	P2l = Counter(list(P2))
	print(len(P2l))
	intrsct = []
	for x in P2l:
		if P1l[x] > 0:
			intrsct.append(x)
	print(len(intrsct))
	union = P1l + P2l

>>>>>>> a3628c7b01b0075fbfbe93241d6ca0c91f29ec47


def calcDiffUw(P1, P2):
	D = 0.0
	P1l = Counter(list(P1))
	#print(P1l)
	print(len(P1l))
	P2l = Counter(list(P2))
	print(len(P2l))
	intrsct = []
	for x in P2l:
		if P1l[x] > 0:
			intrsct.append(x)
	print(len(intrsct))
	union = P1l + P2l
	print(len(union))
	# for x in union:
	# 	if (P1[x] > 0) & (P2[x] > 0):
	# 	# print(((P1[x] - P2[x])/((P1[x] + P2[x])/2))**2)
	# 	# print((2*(P1[x] - P2[x]))/(P1[x] + P2[x]))
			# D += ((2*(P1[x] - P2[x]))/(P1[x] + P2[x]))**2
	# 		# D += 
	print("intersect: ")
	print(len(intrsct))
	D += len(intrsct) / len(union) * 100
	# D += len(intrsct) / len(P2l)
	print(D)
	return D

def normalize(P):
	# unique = len(P)
	# isitone = 0
	tot = sum(P.values())
	for x in P:
		if P[x] == 1:
			P[x] = 0
		else:
			P[x] = P[x]/tot
		# isitone += P[x]
		# print(str(x) + ': ' + str(P[x]))
	return P

# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="File of corpus")
	# parser.add_argument("-text", "--text", help="Text as string")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.corpus)
