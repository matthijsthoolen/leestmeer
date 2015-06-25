# -*- coding: utf-8 -*-

from collections import Counter
from collections import OrderedDict
import sys, getopt, re, pickle,math
from itertools import permutations

# Calculates the Inverse Document Frequency for the corpus POS nGram profiles
def main():
	fm = pickle.load(open('database/www.3fm.nl_POS_nGrams', 'rb'))
	threesixty = pickle.load(open('database/www.360magazine.nl_POS_nGrams', 'rb'))
	bright = pickle.load(open('database/www.bright.nl_POS_nGrams', 'rb'))
	kidsweek = pickle.load(open('database/www.kidsweek.nl_POS_nGrams', 'rb'))
	nos = pickle.load(open('database/www.nos.nl_POS_nGrams', 'rb'))
	nrc = pickle.load(open('database/www.nrc.nl_POS_nGrams', 'rb'))
	sevendays = pickle.load(open('database/www.sevendays.nl_POS_nGrams', 'rb'))
	List = [(fm,'3fm_POS_nGrams'), (threesixty, '360_POS_nGrams'), (bright, 'bright_POS_nGrams'), (kidsweek, 'kidsweek_POS_nGrams'), (nos, 'nos_POS_nGrams'), (nrc, 'nrc_POS_nGrams'), (sevendays, 'sevendays_POS_nGrams')]
	for source,name in List:
		tot = sum(source.values())
		for (x,m) in source:
			freq = 0
			for source2,name2 in List:
				if source2[x] > 0:
					freq += 1
			source[x] = (source[x]/tot) * (1+math.log10(7/freq))
		with open('database\\' +name + '_idf', 'wb') as f:
			pickle.dump(source, f, protocol=2)


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	main()
