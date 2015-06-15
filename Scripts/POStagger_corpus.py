# -*- coding: utf-8 -*-
import pickle, argparse, sys
tagger = pickle.load(open("nltk_data/taggers/conll2002_NaiveBayes_aubt.pickle"))


# USE: 	python POStagger_corpus.py -file path/to/corpus.txt -output /path/to/outputfile.txt
# This File reads in a file line by line, and tries to assign a POS tag to each word.
# The POS tagger is trained using nltk-trainer on the dutch part of the cnll2002 corpus
# All output is then written to a specified output file
def main(corpus,outputFile):
	print('Corpus name is: ' + corpus)
	print('Output file name is: ' + outputFile)
	try:
		inputFile = open(corpus)
		text = inputFile.read()
		getPOStags(text,outputFile)
		inputFile.close()
	except IOError:	
		print('Cannot open ' + corpus)
		sys.exit()


def getPOStags(text,outputFileName):
	try:
		outputFile = open(outputFileName,'w')
		lines = text.splitlines();
		for line in lines:
			# IF line not empty, tag the line with POS tags and write to file
			if line:
				newLine = ""
				transform = tagger.tag(line.decode('latin-1').split())
				for (word, tag) in transform:
					newLine += tag + ' ' 

				outputFile.write(newLine + '\n')
		outputFile.close()
	except IOError:	
		print('Cannot open ' + outputFileName)
		sys.exit()
			



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-file")
	parser.add_argument("-output")
	args = parser.parse_args()
	main(args.file,args.output)

