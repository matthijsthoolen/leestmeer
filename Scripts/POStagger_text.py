# -*- coding: utf-8 -*-
import pickle, argparse, sys, re
tagger = pickle.load(open("nltk_data/taggers/conll2002_NaiveBayes_aubt.pickle"))



# USE: 	import POStagger_text
# 	newPOStags = POStagger_text.getPOStags(text)
# This file accepts a string as input with text, and returns the POS tags of the text
# Done using the nltk toolkit and nltk-trainer with the cnll2002 corpus
def main(text):
	return getPOStags(text)
	

def getPOStags(text):
	POStagText = ""
	lines = text.splitlines();
	for line in lines:
		# IF line not empty, tag the line with POS tags and write to file
		if line:
			# Delete punctuation marks
			#line = line.decode('latin-1')
			line = re.sub(r'[#|&|>|=|(|)|"|:|,|;|-|\+]','',line)
			
			newLine = ""
			#transform = tagger.tag(line.decode('latin-1').split())
			transform = tagger.tag(line.split())
			for (word, tag) in transform:
				POStagText += tag + ' '
			POStagText += '\n' 
	return POStagText


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-text")
	args = parser.parse_args()
	main(args.text)
