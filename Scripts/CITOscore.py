# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math

# This is the main function of the code which calculates the CITO score

def main(corpus, output, common):
	try:
		file = open(corpus, encoding='utf-8', mode='r')
		text = file.read()
		text = text.replace('\n',' ').replace('\"','')
		# text = text.replace('\.\n','\. ').replace('\n','')
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
		sys.exit()

	sentences = re.split('\.[\s+]', text)
	sentences = re.split('\.[\s|\n]|\!+|\?+',text)
	words = re.split('\s',sentences)

	uniqueWords = counter(words)
	typeTokenFrequency = len(uniqueWords) / len(words)
	
	commonFile = open(common, encoding='utf-8', mode='r')
	commonText = file.read()
	commonWords = re.split(',', text)
	totCommonWords = 0
	
	for commonWord in commonWords:
		totCommonWords += uniqueWords[commonWords]
		
	freqCommonWords = totCommonWords / len(words)
	
	wordCount = 0
	lettersCount = 0
	totWords = 0
	totLetters = 0
	totSentences = 0
	avgWords = 0
	avgLetters = 0
	sentences = re.split('\.[\s+]', text)
	sentences = re.split('\.[\s|\n]|\!+|\?+',text)
	
	if output=='debug':
		print(sentences)

	for sentence in sentences:
		# print(sentence)
		if sentence:
			totSentences += 1
			words = re.split('\s',sentence)
			wordCount = len(words)
			for word in words:
				lettersCount = countLetters(word)
				if (lettersCount > 0) & (output=='debug'):
					print(word + ': ' +  str(lettersCount))
				totLetters += lettersCount
			totWords += wordCount

	# print(totNumberofWords)
	# print(totSyllableCount)
	avgWords = totWords/totSentences
	avgLetters = totSyllables/totWords

	if output=='debug':
		print('Average amount of words per sentence: ' + str(avgWords))
		print('Average amount of letters per word: ' + str(avgLetters))
	
	#aviScore = math.ceil(195 - (2 * avgWords) - (200/3*avgLetters)-0.5)
	#aviAge = calcAge(aviScore)
	
	CLIB = 46 - 6.603 * avgLetters + 0.474 * freqCommonWords - 0.365 * typeTokenFrequency + 1.425 * avgWords
	CILT = 105 - (114.49 + 0.28 * freqCommonWords - 12.33 * avgLetters)
	
	if output=='CLIB':
		#print('AVI Score: ' + str(aviScore))
		return CLIB
	elif output=='CILT':
		return CILT


def countLetters(word):
	return len(word)


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="Textfile of corpus", default="input.txt")
	parser.add_argument("-output", "--output", help="Give the type of output, CLIB=CLIB score, CILT=CILT score, debug=info", default="avi")
	parser.add_argument("-common", "--common", help="Textfile of common words", default="common.txt")

	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.corpus, args.output, args.common)