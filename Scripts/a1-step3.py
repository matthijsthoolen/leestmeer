#!/usr/bin/python3

######Authors:##############
#Rutger Kraaijer - 10382259#
###Jan Geestman - 10375406##
###Ruben Blom - 10684980####
############################

from collections import Counter
from collections import OrderedDict
import sys, getopt, argparse
from itertools import permutations

#Main function that prepares the corpus as list, adds start stop to every paragraph and calls functions based on arguments given by the user.
def main(trainCorpus, testCorpus, n, smoothing):
	try:
		file = open(trainCorpus, 'r')
		lines = file.read().splitlines()
		file.close()
		words = []
		prevempty = 1
		for line in lines:
			if line and prevempty == 1:
				prevempty = 0
				i=0
				prepend = []
				while i < n-2:
					prepend = ['<s>'] + prepend
					i += 1
				words.extend(prepend)
				words.append('<s>')
				linewords = line.split()
				words.extend(linewords)
			elif line and prevempty == 0:
				linewords = line.split()
				words.extend(linewords)
			elif not line and prevempty == 0:
				prevempty = 1
				words.append('</s>')

	except IOError: 
		print('Cannot open '+trainCorpus)

	smooth(n, testCorpus, trainCorpus, smoothing)

#Function that allows for two different types of smoothing. 
def smooth(n, testCorpus, trainCorpus, smoothing):
	try:
		file = open(testCorpus, 'r')
		lines = file.read().splitlines()
		file.close()
		words = []
		prevempty = 1
		for line in lines:
			if line and prevempty == 1:
				prevempty = 0
				i=0
				prepend = []
				while i < n-2:
					prepend = ['<s>'] + prepend
					i += 1
				words.extend(prepend)
				words.append('<s>')
				linewords = line.split()
				words.extend(linewords)
			elif line and prevempty == 0:
				linewords = line.split()
				words.extend(linewords)
			elif not line and prevempty == 0:
				prevempty = 1
				words.append('</s>')
	except IOError:
		print('Cannot open '+testCorpus)
	nGrams = makeNgrams(n, words)
	nGramsMin = makeNgrams(n-1, words)
	nGramSum = getSum(nGrams)
	reverseDict = dict()
	if smoothing == "add1":
		nGrams += Counter(list(nGrams))
		nGramsMin += Counter(list(nGramsMin))
	elif smoothing == "gt":
		for k, v in nGrams.items():
			if(v in reverseDict):
				reverseDict[v] = reverseDict[v]+1
			else:
				reverseDict[v] = 1
	nGramSum = getSum(nGrams)
	sentences = []
	sentence = []
	zeroCount = 0
	lineCount = 0
	for word in words:
		sentence.append(word)
		if word == "</s>":
			sentences.append(' '.join(sentence))
			sentence = []
			lineCount += 1
	for sentence in sentences:
		nProb = seqProb(n,sentence,nGrams,nGramsMin,nGramSum,smoothing,reverseDict)
		if nProb == 0:
			zeroCount += 1
	print("'"+str(zeroCount/lineCount*100) + "'% of paragraphs has a probability of 0.0")


#Applies Good Turing Smoothing to given frequency 'r'
def goodTuringSmoothing(r,reverseDict,nGramSum):
	k = 5
	if(r<=k):
		if r==0:
			return reverseDict[1]/nGramSum
		nk = reverseDict[k] if k in reverseDict else 0
		nr = reverseDict[r] if r in reverseDict else 0
		n1 = reverseDict[1] if 1 in reverseDict else 0
		nk1 = reverseDict[k+1] if (k+1) in reverseDict else 0
		nr1 = reverseDict[r+1] if (r+1) in reverseDict else 0
		try:
			return ( (r+1) * (nr1/nr) - r * ( ( (k+1) * nk1 ) / n1) ) / ( 1 - ( ( (k+1) * (nk1) ) / n1) )
		except ZeroDivisionError:
			print("Division by zero error")
			return 0
	return r

#Calculates the probability of an nGram. Has options to apply different smoothing methods
def nGramProb(n,nGrams, nGramsMin, nGramsSum, nGram, smoothing,reverseDict,uniqueMin):
	countn = nGrams[' '.join(nGram)]
	countnMin = nGramsMin[' '.join(nGram[0:n-1])]
	if smoothing == "add1":
		return (countn+1)/(countnMin+1)
	elif smoothing == "gt":
		countn = goodTuringSmoothing(countn,reverseDict,nGramsSum)
		countnMin = goodTuringSmoothing(countnMin,reverseDict,nGramsSum)
		try:	
			return ((countn / countnMin))
		except ZeroDivisionError:
			return 0
	else:
		try:
			return (countn / countnMin)
		except ZeroDivisionError:
			return 0

#Function that calculates the probability of a 'sentence'. Uses the chain rule.
def seqProb(n, sentence, nGrams,nGramsMin,nGramsSum, smoothing,reverseDict):
	nGramIter = makeNgrams(n,sentence.split())
	prob = 1.0
	uniqueMin = getSum(Counter(list(nGramsMin.keys())))
	for nGram in nGramIter:
		nGramprob = nGramProb(n,nGrams, nGramsMin, nGramsSum, nGram.split(),smoothing,reverseDict,uniqueMin)
		prob *= nGramprob
	return prob

#Function that makes n-grams out of 'words'.
def makeNgrams(n, words):
	nGrams = Counter([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])
	return nGrams

#Function that returns the m most common nGrams	
def getMostCommon(nGrams,m):
	return nGrams.most_common(m)

#Function that returns the number of nGrams
def getSum(nGrams):
	return sum(nGrams.values())

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-traincorpus", "-trc", help="Specify training corpus", default="austen.txt")
	parser.add_argument("-testcorpus", "-tec", help="Specify test corpus", default="ja-pers-clean.txt")
	parser.add_argument("-n", type=int, help="Specify n for ngram")
	parser.add_argument("-s","--smoothing", dest="smoothing", help="Type of smoothing to be used")
	args = parser.parse_args()
	main(args.traincorpus, args.testcorpus, args.n, args.smoothing)

