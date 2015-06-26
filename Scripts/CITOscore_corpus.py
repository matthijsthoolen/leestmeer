# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math, pickle

# This is the code which calculates the CITO score for a corpus of text
# and dumps it into a pickled file as a dictionary

def main():
	List = ['www.3fm.nl', 'www.360magazine.nl', 'www.bright.nl', 'www.kidsweek.nl', 'www.nos.nl', 'www.nrc.nl', 'www.sevendays.nl']
	standards = {}
	for source in List:
		print(source)
		corpus = 'database\\' + source
		common = 'database\\common.txt'
		(CLIB, CILT, avgLetters, freqCommonWords, typeTokenFrequency, avgWords) = main2(corpus, common)
		standards['CLIB'] = CLIB
		standards['CILT'] = CILT
		standards['avgLetters'] = avgLetters
		standards['freqCommonWords'] = freqCommonWords
		standards['typeTokenFrequency'] = typeTokenFrequency
		standards['avgWords'] = avgWords
		file = open('database\\' + source + '_averages', 'wb')
		pickle.dump(standards,file,protocol=2)
		file.close()

# Calculates the different values of the CITO scores (CLIB and CILT) and
# returns them as a tuple.

def main2(corpus, common):
	try:
		file = open(corpus, mode='r')
		text = file.read()
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
		sys.exit()

	# Instantiates various variables
	lettersCount = 0
	totLetters = 0
	totSentences = 0
	avgWords = 0.0
	totWords = 0
	avgLetters = 0.0
	allWords = ""

	# Loops through all sentences in the text, removes various punctuation marks
	# and counts the words and letters.
	sentences = text.splitlines()
	for sentence in sentences:
		sentence = re.sub(r'[:|,|;|-]', '', sentence)
		wordCount = 0
		if sentence:
			totSentences += 1
		words = re.split('\s+',sentence)
		wordCount += len(words)
		for word in words:
			totLetters += len(word)
			allWords += word + ' '
		totWords += wordCount

	# Count up all unique words and calculate the type-token-frequency
	uniqueWords = Counter(allWords.split())
	typeTokenFrequency = (len(uniqueWords) * 1.0) / totWords *1.0

	# Opens the text file of common words
	commonFile = open(common, mode='r')
	commonText = commonFile.read()
	commonLines = commonText.splitlines()
	commonWords = re.split(',', commonText)
	totCommonWords = 0

	# Counts how many words in the text are common words
	for commonWord in commonWords:
		totCommonWords += uniqueWords[commonWord]

	# Calculations for some of the variables in the CITO formulas
	# The '*1.0' are fixes for integer divisions
	freqCommonWords = (totCommonWords * 1.0) / (totWords * 1.0)
	avgWords = totWords/(totSentences * 1.0)
	avgLetters = totLetters/(totWords * 1.0)

	# The acutal CITO score calculations
	CLIB = 46 - 6.603 * avgLetters + 0.474 * freqCommonWords - 0.365 * typeTokenFrequency + 1.425 * avgWords
	CILT = 105 - (114.49 + 0.28 * freqCommonWords - 12.33 * avgLetters)

	return (CLIB, CILT, avgLetters, freqCommonWords, typeTokenFrequency, avgWords)

# Code necessary to make this file run from the console
if __name__ == "__main__":
	main()