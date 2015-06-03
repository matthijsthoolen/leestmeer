from collections import Counter
import sys, getopt, argparse, re, math

def main(corpus):
	try:
		file = open(corpus, 'r')
		text = file.read()
		print(text)
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
	
	numberofwords = 0
	syllableCount = 0
	totNumberofWords = 0
	totSyllableCount = 0
	sentenceCount = 0
	avgNumberofwords = 0
	avgSyllableCount = 0
	sentences = re.split('\.\s',text)
	print(sentences)

	for sentence in sentences:
		if sentence:
			sentenceCount += 1
			words = re.split('\s',sentence)
			numberofwords = len(words)
			for word in words:
				syllableCount = countSyllables(word)
				print(word + ': ' +  str(syllableCount))
				totSyllableCount += syllableCount
			totNumberofWords += numberofwords

	# print(totNumberofWords)
	# print(totSyllableCount)
	avgNumberofwords = totNumberofWords/sentenceCount
	avgSyllableCount = totSyllableCount/totNumberofWords

	print(avgNumberofwords)
	print(avgSyllableCount)
	index = math.ceil(195 - (2 * avgNumberofwords) - (200/3*avgSyllableCount))
	print(index)

def countSyllables(word):
	syllableCount = 0
	prevLetter = '0'
	for i in range(len(word)):
		if isSyllable(word[i], prevLetter):
			syllableCount += 1
		prevLetter = word[i]
	return syllableCount


def isSyllable(curLetter, prevLetter):
	vowels = 'aioeuyAIOEUY'
	if vowels.find(prevLetter) == -1:
		if not(vowels.find(curLetter) == -1):
			return True
	else:
		return False

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="Textfile of corpus", default="input.txt")
	args = parser.parse_args()
	main(args.corpus)