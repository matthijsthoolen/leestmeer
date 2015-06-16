# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math, json
import AVIscoreMod2 as AVIscoreMod
import CITOMod2 as CITOMod


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
		text = prepareText(body).decode('latin-1')
		(aviScore,totWords,totSentences,aviAge) = AVIscoreMod.mainAVI(body)
		(CLIB, CILT) = CITOMod.mainCITO(body)
		item['aviScore'] = aviScore
		item['aviAge'] = aviAge
		item['CLIB'] = CLIB
		item['CILT'] = CILT
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
	overall['CILT'] = CILT
	overall['CLIB'] = CLIB
	obj['overall'][0] = overall
	return obj


def prepareText(body):
	text = ""
	bod = re.split('\.[\s|\n]+|\!+[\s|\n]+|\?+[\s|\n]+',body)
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
