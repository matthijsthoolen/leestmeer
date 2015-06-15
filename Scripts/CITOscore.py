# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math

# This is the main function of the code which calculates the CITO score

def main(corpus, output, common):
	try:
		file = open(corpus, mode='r')
		text = file.read()
		# text = text.replace('\.\n','\. ').replace('\n','')
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
		sys.exit()

	lettersCount = 0
	totLetters = 0
	totSentences = 0
	avgWords = 0
	totWords = 0
	avgLetters = 0

	sentences = text.splitlines()
	for sentence in sentences:
		wordCount = 0
		if sentence:
			totSentences += 1

		words = re.split('\s+',sentence)
		wordCount += len(words)
		for word in words:
			lettersCount = countLetters(word)
			if (lettersCount > 0) & (output=='debug'):
				print(word + ': ' +  str(lettersCount))
			totLetters += lettersCount
		totWords += wordCount

	uniqueWords = Counter(words)
	typeTokenFrequency = len(uniqueWords) / totWords
	
	commonFile = open(common, encoding='utf-8', mode='r')
	commonText = commonFile.read()
	commonWords = re.split(',', commonText)
	totCommonWords = 0
	
	for commonWord in commonWords:
		totCommonWords += uniqueWords[commonWord]
		
	freqCommonWords = totCommonWords / totWords
	
	if output=='debug':
		print(sentences)

	avgWords = totWords/totSentences
	avgLetters = totLetters/totWords

	if output=='debug':
		print('Average amount of words per sentence: ' + str(avgWords))
		print('Average amount of letters per word: ' + str(avgLetters))
	
	print(avgLetters)
	print(freqCommonWords)
	print(typeTokenFrequency)
	print(avgWords)
	CLIB = 46 - 6.603 * avgLetters + 0.474 * freqCommonWords - 0.365 * typeTokenFrequency + 1.425 * avgWords
	CILT = 105 - (114.49 + 0.28 * freqCommonWords - 12.33 * avgLetters)
	
	if output=='CLIB':
		print(CLIB)
		return CLIB
	elif output=='CILT':
		print(CILT)
		return CILT


def countLetters(word):
	return len(word)


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="Textfile of corpus", default="input.txt")
	parser.add_argument("-output", "--output", help="Give the type of output, CLIB=CLIB score, CILT=CILT score, debug=info", default="debug")
	parser.add_argument("-common", "--common", help="Textfile of common words", default="common.txt")
	args = parser.parse_args()
	main(args.corpus, args.output, args.common)