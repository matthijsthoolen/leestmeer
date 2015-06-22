# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math, json, pickle
import AVIscoreMod2 as AVIscoreMod
import CITOMod2 as CITOMod
import POStagger_text as tagger
import ngramProfiler 
import textDifferenceMod


# accepts a JSON object, unpacks it, analyzes it and sends it back
def main(obj):
	index = -1
	avgSentence = 0
	numSentences = 0
	totalText = ""
	parObj = obj['text']
	corpus = obj['info'][0]['corpusSet']
	corpus = 'database\\' + corpus
	for item in parObj:
		index += 1
		body = item['paragraph']		
		if body:
			print("print die paragraph")
			text = prepareText(body).decode('latin-1')
											
			# Calculate metrics of current text
			(aviScore,totWords,totSentences,aviAge) = AVIscoreMod.mainAVI(body)
			(CLIB, CILT, avgLetters, freqCommonWords, typeTokenFrequency, avgWords) = CITOMod.mainCITO(body)
											
			# Do a POStag analysis on the text, and calculate ngrams of those
			POStags = tagger.getPOStags(text)
			nGrams = ngramProfiler.main(POStags,3)
			resemblance = textDifferenceMod.main(corpus + '_POS_nGrams',text)
			
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
			totalText += body
			totalText += '\n\n'
			obj['text'][index] = item

	overall = obj['overall'][0]
	(aviScore,totWords,totSentences,aviAge) = AVIscoreMod.mainAVI(totalText)
	(CLIB, CILT, avgLetters, freqCommonWords, typeTokenFrequency, avgWords) = CITOMod.mainCITO(totalText)
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

	corpusText = obj['corpus'][0]
	Set = obj['info'][0]['corpusSet'] 
	corpusSet = pickle.load(open('database\\' + Set, 'rb'))
	corpusText['avgLetters'] = corpusSet['avgLetters']
	corpusText['freqCommonWords'] = corpusSet['freqCommonWords']
	corpusText['typeTokenFrequency'] = corpusSet['typeTokenFrequency']
	corpusText['avgWords'] = corpusSet['avgWords']
	obj['corpus'][0] = corpusText
	return obj

# prepare text by putting each sentence on a new line
def prepareText(body):
	text = ""
	body.replace("&nbsp;"," ")
	bod = re.split('\.[\s|\n]+|\!+[\s|\n]+|\?+[\s|\n]+',body)
	# bod = re.sub(r':|,|;|-', '',bod)
	for line in bod:
		line += '\n'
		text += line
	print(text)
	return text

# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-obj", "--obj", help="Object to be analyzed")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.obj)
