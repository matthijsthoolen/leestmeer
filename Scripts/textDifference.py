# -*- coding: utf-8 -*-

from collections import Counter
import sys, argparse, re, pickle, math
import ngramProfiler
import ast

def main(corpus):
	try:
		with open(corpus, 'rb') as f:

			# get corpus, is a list of tupples
			P1 = pickle.load(f)

			paragraph = 'database/tests/3fm_POS'
			print 'Score of ', corpus, ' for ',paragraph
			# analyze current text, returns counter
			file = open(paragraph, 'r')
			text = file.read()
			file.close()
			P2 = ngramProfiler.main(text,3)

	except IOError: 
		print('Cannot open '+corpus)
	calcDiffUw(P1, P2)



def calcDiffUw(P1, P2):
	D = 0.0

	P2l = Counter(list(P2))

	intrsct = []

	[ngramsCorpus, ngramFrCorpus] = zip(*P1)

	# Find intersection between P1 and P2
	for x in P2l:
		if x in ngramsCorpus:
			intrsct.append(x)

	intrsct = len(intrsct)
	print'intrsct:', intrsct

	union = len(P1) + len(P2l)
	# print('union:')
	# print(union)

	# Sorensen-Dice coefficient
	D1 = (intrsct * 2.0) / union * 100
	print 'Sorensen-Dice coefficient:', D1

	# calculate resemblance with Jaccard index
	#D2 = (intrsct * 1.0) / union * 100
	#print 'jaccard index:', D2

	# calculate overlap coefficient
	D3 = (intrsct * 1.0) / min([len(P1),len(P2l)]) * 100
	print 'Overlap coefficient:', D3

	# calculate the Tversky index
	D4 = (intrsct * 1.0) / (intrsct + (len(P1)-intrsct) + (len(P2l)-intrsct)) * 100
	print 'Tversky index:', D4

	return D1


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="File of corpus")
	# parser.add_argument("-text", "--text", help="Text as string")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.corpus)
