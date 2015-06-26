# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math, json, pickle
import AVIscore
import CITOscore_text
import POStagger_text as tagger
import ngramProfiler_text
import textDifference


# accepts a JSON object, unpacks it, analyzes it and sends it back
def main(obj):
	standardDeviationLetters = 1.2 # still need to calculate this
	standardDeviationWords = 1.0 # still need to calculate this
	avgWordsThreshold = 2.1 + standardDeviationWords
	avgLettersThreshold = 0.0

	index = -1
	avgSentence = 0
	numSentences = 0
	totalText = ""
	parObj = obj['text']
	corpus = obj['info']['corpusSet']
	corpus = 'database/' + corpus
	print 'corpus path:',corpus

	# Get corpus statistics
	corpusText = obj['corpus'][0]
	corpusSet = pickle.load(open(corpus + '_averages', 'rb'))
	corpusText['avgLetters'] = corpusSet['avgLetters']
	corpusText['freqCommonWords'] = corpusSet['freqCommonWords']
	corpusText['typeTokenFrequency'] = corpusSet['typeTokenFrequency']
	corpusText['avgWords'] = corpusSet['avgWords']
	corpusText['CILT'] = corpusSet['CILT']
	corpusText['CLIB'] = corpusSet['CLIB']
	obj['corpus'][0] = corpusText

	# Analyze each paragraph
	for item in parObj:
		hasContent = False
		index += 1
		body = item['paragraph']		
		testSen = body.splitlines()
		for sen in testSen:
			if sen:
				hasContent = True
		if hasContent:
			text = body.encode('utf-8')
			text = prepareText(body)
			avgLettersThreshold = 0.0
											
			# Calculate metrics of current text
			(aviScore,totWords,totSentences,aviAge) = AVIscore.mainAVI(text)
			(CLIB, CILT, avgLetters, freqCommonWords, typeTokenFrequency, avgWords) = CITOscore_text.mainCITO(text)
											
			# Do a POStag analysis on the text, and calculate ngrams of those
			POStags = tagger.getPOStags(text)
			nGrams = ngramProfiler_text.main(POStags,3)
			resemblance = textDifference.main(corpus + '_POS_nGrams',POStags)
			#print 'paragraph resemblance:',resemblance


			# verbeteringen:
			# freqCommonWords -> sidebar (of synoniemen)
			# TypeTokenFrequency -> sidebar (of (anti-)synoniemen)
			# avgLetters 	-> te lang: lange woorden + sidebar
			#		-> te kort: sidebar
			# avgWords -> 

			# Delete dummy highlights from JSON object, and set the word
			item['highlights'] = []	
			#item['checks'] = {}
			item['checks']['wordHighlights'] = False
			item['checks']['sentenceHighlights'] = False
			item['checks']['freqCommonWordsHighlights'] = False
			item['checks']['typeTokenFrequencyHighlights'] = False
				
			print('Highlights:')
			print(item['highlights'])

			wordHighlights= False
			sentenceHighlights = False
			
			# calculate difference between corpus and paragraph
			if math.fabs(corpusSet['CILT'] - CILT) > 5:
				item['checks']['freqCommonWordsHighlights'] = True
				wordHighlights = True
				avgLettersThreshold = 0.405 + standardDeviationLetters
				print '\nCILT score off, is:', CILT, 'should be:',corpusSet['CILT']
				print 'Frequency common words off, is:', freqCommonWords, ' should be:', corpusSet['freqCommonWords'] 
				print 'avgLetters per word off, is:', avgLetters, ' should be:', corpusSet['avgLetters'],'\n'
			if math.fabs(corpusSet['CLIB'] - CLIB) > 3:
				item['checks']['typeTokenFrequencyHighlights'] = True
				item['checks']['freqCommonWordsHighlights'] = True
				wordHighlights = True
				sentenceHighlights = True
				avgLettersThreshold = 0.45432 + standardDeviationLetters
				print '\nCLIB score off, is:', CLIB, 'should be:',corpusSet['CLIB']
				print 'Frequency common words off, is:',freqCommonWords, ' should be:', corpusSet['freqCommonWords'] 
				print 'avgLetters per word off, is:', avgLetters, ' should be:', corpusSet['avgLetters']
				print 'typeTokenFrequency off, is:', typeTokenFrequency, ' should be:',corpusSet['typeTokenFrequency']
				print 'avgWords per sentence off, is:', avgWords, ' should be:', corpusSet['avgWords'], '\n'


			# Find words which deviate from the average in length, and put them in the JSON object
			if(((avgLetters - corpusSet['avgLetters']) > avgLettersThreshold) and wordHighlights):
				item['checks']['wordHighlights'] = True
				highlightWords = findLongWords(text, corpusSet['avgLetters'],avgLettersThreshold)
				for word in highlightWords:
					item['highlights'].append({'text':word, 'color':1, 'hint':1})

			# Find sentences which deviate from the average in length, and put them in the JSON object
			if((math.fabs(avgWords - corpusSet['avgWords']) > avgWordsThreshold) and sentenceHighlights):
				item['checks']['sentenceHighlights'] = True
				highlightSentences = findLongSentences(text, avgWords, corpusSet['avgWords'],avgWordsThreshold)
				for sentence in highlightSentences:
					item['highlights'].append({'text':sentence, 'color':5, 'hint':5})

			# Put data in the JSON object
			item['aviScore'] = aviScore
			item['aviAge'] = aviAge
			item['clibScore'] = CLIB
			item['ciltScore'] = CILT
			item['resemblance'] = resemblance
			item['analytics']['totalWords'] = totWords
			item['analytics']['avgWords'] = avgWords
			item['analytics']['avgLetters'] = avgLetters
			item['analytics']['freqCommonWords'] = freqCommonWords
			item['analytics']['typeTokenFrequency'] = typeTokenFrequency
			totalText += text
			totalText += '\n\n'
			obj['text'][index] = item

			



	overall = obj['overall'][0]
	(aviScore,totWords,totSentences,aviAge) = AVIscore.mainAVI(totalText)
	(CLIB, CILT, avgLetters, freqCommonWords, typeTokenFrequency, avgWords) = CITOscore_text.mainCITO(totalText)
	overall['aviScore'] = aviScore
	overall['aviAge'] = aviAge
	index = -1
	for item in obj['text']:
		index += 1
		if (item['aviScore'] > overall['aviScore']):
			obj['text'][index]['Colour'] = '#FF0000'
		elif (item['aviScore'] < overall['aviScore']):
			obj['text'][index]['Colour'] = '#0000FF'
		else:
			obj['text'][index]['Colour'] = '#FFFFFF'
	overall['ciltScore'] = CILT
	overall['clibScore'] = CLIB
	obj['overall'][0] = overall

	#print obj

	return obj

# prepare text by putting each sentence on a new line
def prepareText(body):
	text = ""
	body.replace("&nbsp;"," ")
	bod = re.split('\.[\s|\n]+|\!+[\s|\n]+|\?+[\s|\n]+',body)
	# bod = re.sub(r':|,|;|-', '',bod)
	for line in bod:
		line += '\n'
		#print(line)
		text += line
	#print(text)
	return text


# find words which are too long in the current paragraph
def findLongWords(text, avgLettersCorpus, avgLettersThreshold):

	highlightWords = []
	sentences = text.splitlines()

	for sentence in sentences:
		if sentence:
			words = re.split('\s',sentence)
			for word in words:
				if (len(word) - avgLettersCorpus) > avgLettersThreshold:
					highlightWords.append(word)

	return highlightWords
	
	

# find setences which are too short or long, depending on the deviation of the average
def findLongSentences(text, avgWords, avgWordsCorpus, avgWordsThreshold):
	
	sentenceLowerHigher = avgWords - avgWordsCorpus
	sentences = text.splitlines()
	highlightSentences = []

	for sentence in sentences:
		if sentence:
			# hightlight long sentences if the average sentence is too long
			if ((len(sentence) - avgWordsCorpus) > avgWordsThreshold) and (sentenceLowerHigher > 0):
					highlightSentences.append(sentence)
			# hightlight short sentences if the average sentence is too short
			if ((len(sentence) - avgWordsCorpus) < -avgWordsThreshold) and (sentenceLowerHigher < 0):
					highlightSentences.append(sentence)
	
	return highlightSentences



# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-obj", "--obj", help="Object to be analyzed")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.obj)
