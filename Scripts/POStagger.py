# -*- coding: utf-8 -*-
import pickle, argparse, sys
tagger = pickle.load(open("nltk_data/taggers/conll2002_NaiveBayes_aubt.pickle"))


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
			print(type(line))
			# IF line not empty, tag the line with POS tags and write to file
			if line:
				newLine = ""
				transform = tagger.tag(line.split())
				for (word, tag) in transform:
					newLine += tag
					newLine += ' ' 
				print(newLine)
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

