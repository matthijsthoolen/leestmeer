from collections import Counter
import sys, getopt, argparse, re, math

# This is the main function of the code which calculates the AVI score
# of a body of text. It does this by first calculating the average
# number of words per sentence and the average number of syllables
# per word. These two numbers are used in the final equation that 
# computes the AVI score.
def main(corpus):
	try:
		file = open(corpus, encoding='utf-8', mode='r')
		text = file.read()
		text = text.replace('\n',' ').replace('\"','')
		# text = text.replace('\.\n','\. ').replace('\n','')
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
		sys.exit()

	wordCount = 0
	syllableCount = 0
	totWords = 0
	totSyllables = 0
	totSentences = 0
	avgWords = 0
	avgSyllables = 0
	sentences = re.split('\.[\s+]', text)
	sentences = re.split('\.[\s|\n]|\!+|\?+',text)
	print(sentences)

	for sentence in sentences:
		# print(sentence)
		if sentence:
			totSentences += 1
			words = re.split('\s',sentence)
			wordCount = len(words)
			for word in words:
				syllableCount = countSyllables(word)
				if syllableCount > 0:
					print(word + ': ' +  str(syllableCount))
				totSyllables += syllableCount
			totWords += wordCount

	# print(totNumberofWords)
	# print(totSyllableCount)
	avgWords = totWords/totSentences
	avgSyllables = totSyllables/totWords

	print('Average amount of words per sentence: ' + str(avgWords))
	print('Average amount of syllables per word: ' + str(avgSyllables))
	aviScore = math.ceil(195 - (2 * avgWords) - (200/3*avgSyllables))
	print('AVI Score: ' + str(aviScore))

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
# an 'A' following an 'E', as well as an 'Ë' or 'Ï' can denote a new syllable
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
	parser.add_argument("-corpus", "--corpus", help="Textfile of corpus", default="input.txt")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.corpus)