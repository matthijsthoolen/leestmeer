# -*- coding: utf-8 -*-
import sys, getopt, argparse, re, pickle, urllib.parse
from html.parser import HTMLParser as HP
import html
import xml.etree.ElementTree as ET
import AVIscoreMod

def main(corpus):
	file = open(corpus, 'r')
	body = file.read()
	file.close()
	bod = re.split('\.[\s|\n]|\!+|\?+',body)
	file = open(corpus + '_prep' , 'w')
	for line in bod:
		file.write(line)
		file.write('\n')
	file.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="Pickled file", default="articles.pickle")
	# Name and location of the pickled articles file
	args = parser.parse_args()
	main(args.corpus)