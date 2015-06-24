# -*- coding: utf-8 -*-

from collections import Counter
import sys, getopt, argparse, re, math


# This is the main function of the code which calculates the AVI score
# of a body of text. It does this by first calculating the average
# number of words per sentence and the average number of syllables
# per word. These two numbers are used in the final equation that 
# computes the AVI score.

def mainAVI(text):
	wordCount = 0
	syllableCount = 0
	totWords = 0
	totSyllables = 0
	totSentences = 0
	avgWords = 0
	avgSyllables = 0

	#print(text)
	sentences = text.splitlines()

	for sentence in sentences:
		if sentence:
			totSentences += 1
			words = re.split('\s',sentence)
			wordCount = len(words)
			for word in words:
				syllableCount = countSyllables(word)
				totSyllables += syllableCount
			totWords += wordCount

	avgWords = totWords / (totSentences*1.0)
		
	avgSyllables = totSyllables / (totWords*1.0)

	#print 'avgSyllables:',avgSyllables, 'avgWords', avgWords

	aviScore = math.ceil(195 - (2 * avgWords) - (200/3*avgSyllables)-0.5)
	aviAge = calcAge(aviScore)
	tup = (aviScore,totWords,totSentences,aviAge)
	return tup
		
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
	curLetter = curLetter.encode('utf-8')#.decode('latin-1')
	prevLetter = prevLetter.encode('utf-8')#.decode('latin-1')
	e = 'E'
	a = 'A'
# 	trema = 'ËÏ'
	if not(e.find(prevLetter.upper()) == -1):
		if not(a.find(curLetter.upper()) == -1):
			return  True	
# 	if not(trema.find(curLetter.upper()) == -1):
# 		return True
 	return False


# This function states the commandline arguments that are needed
# for the program to run.
# if __name__ == "__main__":
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("-obj", "--obj", help="Object or textfile", default="text1.txt")
# 	parser.add_argument("-output", "--output", help="Give the type of output, avi=avi score, age=avi age, debug=info", default="avi")
# 	parser.add_argument("-option", "--option", help="Type of the object", default="file")
# 	#Name and location of the text file to be parsed
# 	args = parser.parse_args()
# 	main(args.obj, args.output, args.option)
