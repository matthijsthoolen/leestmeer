from collections import Counter
import sys, getopt, argparse, re, math

# This is the main function of the code which calculates the CITO score

def mainCITO(text):
	common = 'database/common.txt'
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
			lettersCount = len(word)
			totLetters += lettersCount
		totWords += wordCount

	uniqueWords = Counter(words)
	typeTokenFrequency = len(uniqueWords) / totWords
	
	commonFile = open(common)
	commonText = commonFile.read()
	commonWords = re.split(',', commonText)
	totCommonWords = 0
	
	for commonWord in commonWords:
		totCommonWords += uniqueWords[commonWord]
		
	freqCommonWords = totCommonWords / totWords

	avgWords = totWords/totSentences
	avgLetters = totLetters/totWords

	CLIB = 46 - 6.603 * avgLetters + 0.474 * freqCommonWords - 0.365 * typeTokenFrequency + 1.425 * avgWords
	CILT = 105 - (114.49 + 0.28 * freqCommonWords - 12.33 * avgLetters)

	return (CLIB, CILT)


# This function states the commandline arguments that are needed
# for the program to run.
# if __name__ == "__main__":
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("-corpus", "--corpus", help="Textfile of corpus", default="input.txt")
# 	parser.add_argument("-output", "--output", help="Give the type of output, CLIB=CLIB score, CILT=CILT score, debug=info", default="debug")
# 	parser.add_argument("-common", "--common", help="Textfile of common words", default="common.txt")
# 	args = parser.parse_args()
# 	main(args.corpus, args.output, args.common)