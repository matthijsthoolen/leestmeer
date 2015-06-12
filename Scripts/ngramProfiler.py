from collections import Counter
from collections import OrderedDict
import sys, getopt, argparse
from itertools import permutations

#Main function that prepares the corpus as list, adds start stop to every paragraph and calls functions based on arguments given by the user.
def main(corpus, n):
	try:
		file = open(corpus, 'r', encoding='utf-8', errors='ignore')
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
		print('Cannot open '+corpus)
	nGrams = makeNgrams(n, words)
	del nGrams['</s> <s> <s>']
	# for key,item in nGrams.items():
	# 	if item > 0:
	# 		print(str(key) + ': ' + str(nGrams[key]))
	# print(nGrams)
	file = open(corpus + '_nGrams', 'w')
	# for key,item in nGrams.items():
	file.write(str(nGrams))
	file.close()		



#Function that makes n-grams out of 'words'.
def makeNgrams(n, words):
	nGrams = Counter([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])
	return nGrams

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", type=int, help="Specify n for ngram")
	parser.add_argument("-corpus", dest="corpus", help="corpus name")
	args = parser.parse_args()
	main(args.corpus, args.n)