# -*- coding: utf-8 -*-

from collections import Counter
import sys, argparse, re, pickle
import ngramProfiler
import ast

def main(corpus):
	try:
		with open(corpus, 'rb') as f:
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


def calcDiff(P1, P2):
	D = 0.0
	part = 0.0
	union = P1 + P2
	for x in union:
		# print(P1[x] - P2[x])
		part is ((P1[x] - P2[x])/((P1[x] + P2[x])/2))**2
		D += part
	# print(D)
	return D

def normalize(P):
	unique = len(P)
	tot = sum(P.values())
	for x in P:
		P[x] = P[x]/tot
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
