from collections import Counter
import sys, getopt, argparse

def main(corpus, n, m):
	try:
		file = open(corpus, 'r', encoding='utf-8', errors='ignore')
		words = file.read().split()
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
		
	nGrams = makeNgrams(n,corpus)
	mostCommon = getMostCommon(nGrams,m)
	nGramsSum = getSum(nGrams)
	print(nGrams)
	print(mostCommon)
	print(nGramsSum)

def makeNgrams(n, fileName):
	with open(fileName, "r") as corpus:
		wordList = [w for ln in corpus for w in ln.split()]
	nGrams = Counter([' '.join(wordList[i:i+n]) for i in range(len(wordList)-n+1)])
	return nGrams
	
def getMostCommon(nGrams,m):
	return nGrams.most_common(m)

def getSum(nGrams):
	return sum(nGrams.values())

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="Textfile of corpus", default="austen.txt")
	parser.add_argument("-n", type=int, help="Specify n for ngram", default=2)
	parser.add_argument("-m", type=int, help="Specify m", default=1)
	args = parser.parse_args()
	main(args.corpus, args.n, args.m)
