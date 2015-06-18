from collections import Counter
from collections import OrderedDict
import sys, getopt, argparse, re
from itertools import permutations

# Prepares an already tagged corpus and creates N-Gram model
def main(text, n):
	words = prepareText(text,n)
	nGrams = makeNgrams(n, words)
	# if n == 3:
	# 	del nGrams['</s> <s> <s>']
	c = Counter(nGrams)
	return c


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

#Function that makes n-grams out of 'words'.
def makeNgrams(n, words):
	nGrams = Counter([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])
	return nGrams

# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# parser.add_argument("-corpus", "--corpus", help="File of corpus")
	parser.add_argument("-text", "--text", help="Text as string")
	parser.add_argument("-n")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.text, args.n)