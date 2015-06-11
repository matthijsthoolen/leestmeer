# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math


# This is the main function of the code which calculates the AVI score
# of a body of text. It does this by first calculating the average
# number of words per sentence and the average number of syllables
# per word. These two numbers are used in the final equation that 
# computes the AVI score.
def main(obj, output, option):
	if option=='file':
		return mainF(obj, output)
	elif option=='object':
		return mainO(obj)
	elif option=='text':
		(aviScore,totWords,totSentences,aviAge) = mainAVI(obj,'avi')
		return (aviScore,aviAge)
	else:
		print('Wrong option defined')
		print('Expected: "file", "object" or "text"')
		print('Got: ' + str(option))

def mainO(x):
	avgSentence = 0
	numSentences = 0
	aviDiff = 0
	index = -1
	totalText = ""
	textarray = x['text']
	for item in textarray:
		index+=1
		body = item['paragraph'].encode("utf-8")
		# print(item['aviscore'])
		(aviScore,totWords,totSentences,aviAge) = mainAVI(body, 'avi')
		item['aviScore'] = aviScore
		item['aviAge'] = aviAge
		item['analytics']['totalWords'] = totWords
		avgSentence is totWords/totSentences
		item['analytics']['avgSentence'] = avgSentence
		totalText += body
		totalText += '\n\n'
		x['text'][index] = item
	(aviScore,totWords,totSentences,aviAge)= mainAVI(totalText, 'avi')
	x['overall'][0]['aviScore'] = aviScore
	numSentences is index+1
	x['overall'][0]['analytics']['paragraphs'] = numSentences
	x['overall'][0]['aviAge'] = aviAge 
	for item in x['text']:
		aviDiff is item['aviAge'] - x['overall'][0]['aviAge']
		if (aviDiff > 1) | (aviDiff < -1):
			item['paragraphColour'] = '#FF0000'
		else:
			item['paragraphColour'] = '#FFFFFF'
	return x

def mainF(corpus,output):
	try:
		file = open(corpus, encoding='utf-8', mode='r')
		text = file.read()
		text = text.replace('\n',' ').replace('\"','')
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
		sys.exit()
	if output=='avi':
		(aviScore,totWords,totSentences,aviAge) = mainAVI(text, output)
		return aviScore
	else:
		return mainAVI(text, output)

def mainAVI(text, output):
	wordCount = 0
	syllableCount = 0
	totWords = 0
	totSyllables = 0
	totSentences = 0
	avgWords = 0
	avgSyllables = 0
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
				syllableCount = countSyllables(word)
				if (syllableCount > 0) & (output=='debug'):
					print(word + ': ' +  str(syllableCount))
				totSyllables += syllableCount
			totWords += wordCount

	# print(totNumberofWords)
	# print(totSyllableCount)
	avgWords = totWords/totSentences
	avgSyllables = totSyllables/totWords

	if output=='debug':
		print('Average amount of words per sentence: ' + str(avgWords))
		print('Average amount of syllables per word: ' + str(avgSyllables))
	
	aviScore = math.ceil(195 - (2 * avgWords) - (200/3*avgSyllables)-0.5)
	aviAge = calcAge(aviScore)
	tup = (aviScore,totWords,totSentences,aviAge)
	
	if output=='avi':
		# print('AVI Score: ' + str(aviScore))
		return tup
	elif output=='age':
		if (aviAge > 0):
			# print('AVI Age: ' + str(aviAge))
			return aviAge
		else:
			# print('AVI Age: unspecified')
			return 'unspecified'
			
#aviScore is used to calculate the AVI Age
def calcAge(aviScore):
	if 127 >= aviScore >= 123:
		return 1
	elif 123 >= aviScore >= 112:
		return 2
	elif 112 >= aviScore >= 108:
		return 3
	elif 108 >= aviScore >= 100:
		return 4
	elif 99 >= aviScore >= 94:
		return 5
	elif 93 >= aviScore >= 89:
		return 6
	elif 88 >= aviScore >= 84:
		return 7
	elif 83 >= aviScore >= 79:
		return 8
	elif 78 >= aviScore >= 74:
		return 9
	else:
		return 0


# This function is used in order to count the number of syllables a
# word contains. It does this by evaluating each letter in the word
# and calling isSyllable/2 with that letter and the one before it
def countSyllables(word):
	syllableCount = 0
	prevLetter = '0'
	for i in range(len(word)):
		if isSyllable(word[i], prevLetter):
			syllableCount += 1
		prevLetter = word[i]
	return syllableCount

# Checks if the current letter is the start of a syllable
# This is defined as being the case when the curLetter is a vowel
# while the prevLetter is not
def isSyllable(curLetter, prevLetter):
	vowels = 'AIOEUY'
	if vowels.find(prevLetter.upper()) == -1:
		if not(vowels.find(curLetter.upper()) == -1):
			return True
	elif syllableExceptions(curLetter, prevLetter):
		return True	
	else:
		return False

# This function contains several exceptions in the dutch language that
# count as new syllables. Rather than being a vowel followed by a consonant,
# an 'A' following an 'E', as well as those letters with diaeresis can denote a new syllable
def syllableExceptions(curLetter, prevLetter):
	e = 'E'
	a = 'A'
	trema = 'ËÏ'
	# print(curLetter)
	# print('found: ' + str(trema.find(curLetter)))
	if not(e.find(prevLetter.upper()) == -1):
		# print('1')
		if not(a.find(curLetter.upper()) == -1):
			# print('2')
			return  True	

	if not(trema.find(curLetter.upper()) == -1):
		# print('3')
		return True
	
	# print('4')
	return False


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-obj", "--obj", help="Object or textfile", default="text1.txt")
	parser.add_argument("-output", "--output", help="Give the type of output, avi=avi score, age=avi age, debug=info", default="avi")
	parser.add_argument("-option", "--option", help="Type of the object", default="file")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.obj, args.output, args.option)