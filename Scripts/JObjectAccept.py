# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math, json
import AVIscoreMod2 as AVIscoreMod
import CITOMod2 as CITOMod
import POStagger_text as tagger


# def main(f):
# 	obj = json.loads(f)
# 	print('hello')
# 	print(mainB(obj)['overall'][aviScore])

def main(obj):
	index = -1
	avgSentence = 0
	numSentences = 0
	totalText = ""
	parObj = obj['text']
	for item in parObj:
		index += 1
		body = item['paragraph']

		if body:

			
			text = prepareText(body).decode('latin-1')
			(aviScore,totWords,totSentences,aviAge) = AVIscoreMod.mainAVI(body)
			(CLIB, CILT) = CITOMod.mainCITO(body)

			item['aviScore'] = aviScore
			item['aviAge'] = aviAge
			item['clibScore'] = CLIB
			item['ciltScore'] = CILT
			item['analytics']['totalWords'] = totWords
			avgSentence is totWords/totSentences
			item['analytics']['avgSentence'] = avgSentence
			totalText += body
			totalText += '\n\n'
			obj['text'][index] = item
	(aviScore,totWords,totSentences,aviAge) = AVIscoreMod.mainAVI(totalText)
	(CLIB, CILT) = CITOMod.mainCITO(totalText)
	overall = obj['overall'][0]
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
	return obj


def prepareText(body):
	text = ""
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
