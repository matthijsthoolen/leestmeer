# -*- coding: utf-8 -*-

from collections import Counter
from collections import OrderedDict
import sys, getopt, argparse, re, pickle, math
from itertools import permutations

# Prepares an already tagged corpus and creates N-Gram model
def main(corpus, n):
	file = open(corpus, 'r')
	text = file.read()
	file.close()
	words = prepareText(text, int(n))

	# Get n-gram, returns Counter with top 600 ngrams
	nGrams = makeNgrams(int(n), words)
	file = open(corpus+'_nGrams', 'wb')
	pickle.dump(nGrams,file, protocol=2)
	file.close()


# append start/end symbols to each sentence
def prepareText(corpus, n):
	lines = corpus.splitlines()
	words = []
	for line in lines:
		if line:
			wordline = re.split(' ', line)
			i=0
			prepend = []
			while i < n-2:
				words.append('<s>')
				i += 1
			words.append('<s>')
			for x in wordline:
				if x:
					words.append(x)
			words.append('</s>')
	return words

# Function that makes n-grams out of 'words'.
def makeNgrams(n, words):
	# Make n-grams of words, and ignore n-grams only consisting of start/ends and 
	# n-grams only existing of unknown words
	ignore = {'</s> <s> <s>','</s> <s> <s> <s>','Misc Misc Misc'}
	nGrams = Counter([' '.join(words[i:i+n]) for i in range(len(words)-n+1) if ' '.join(words[i:i+n]) not in ignore])
	
	print("Unique nGrams:")
	print(len(nGrams))
	# Define corpus as 600 most common nGrams, (601 with </s> <s> <s>)
	# E.g. Politie has 367 unique sets, bright 800	
	nGrams = nGrams.most_common(600)
	nGramsC = Counter()
	for i in range(0, len(nGrams)):
		nGramsC[nGrams[i][0]] = nGrams[i][1]
	return nGramsC

# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# parser.add_argument("-corpus", "--corpus", help="File of corpus")
	parser.add_argument("-corpus", "--corpus", help="file")
	parser.add_argument("-n")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.corpus, args.n)