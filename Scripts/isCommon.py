from collections import Counter
import sys, getopt, argparse, re, math

# This is the main function of the code which calculates the AVI score
# of a body of text. It does this by first calculating the average
# number of words per sentence and the average number of syllables
# per word. These two numbers are used in the final equation that 
# computes the AVI score.
def main(word,common):
	try:
		file = open(common, encoding='utf-8', mode='r')
		text = file.read()
		text = text.replace(' ', '')
		# text = text.replace('\.\n','\. ').replace('\n','')
		file.close()	
	except IOError:	
		print('Cannot open '+common)
		sys.exit()
	print(word)
	commonWords = re.split(',', text)
	if word in commonWords:
		print('common')
	else:
		print('uncommon')

# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-word", help="Word", default="aap")
	parser.add_argument("-common", "--common", help="Textfile of common words", default="common.txt")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.word, args.common)