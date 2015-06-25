from collections import Counter
import sys, argparse, re, math, csv
import cPickle as pickle
import ast

def main():
	print(sys.getfilesystemencoding())
	fm = pickle.load(open('database/www.3fm.nl_averages', 'rb'))
	threesixty = pickle.load(open('database/www.360magazine.nl_averages', 'rb'))
	bright = pickle.load(open('database/www.bright.nl_averages', 'rb'))
	kidsweek = pickle.load(open('database/www.kidsweek.nl_averages', 'rb'))
	nos = pickle.load(open('database/www.nos.nl_averages', 'rb'))
	nrc = pickle.load(open('database/www.nrc.nl_averages', 'rb'))
	sevendays = pickle.load(open('database/www.sevendays.nl_averages', 'rb'))

	List = [(fm,'3fm_averages'), (threesixty, '360_averages'), (bright, 'bright_averages'), (kidsweek, 'kidsweek_averages'), (nos, 'nos_averages'), (nrc, 'nrc_averages'), (sevendays, 'sevendays_averages')]
	
	dicts = [fm,threesixty,bright,kidsweek,nos,nrc,sevendays]

	with open('averages.csv', 'wb') as g:
		writer = csv.writer(g, delimiter='\t')
		writer.writerow(['ID', '3fm', '360magazine', 'bright', 'kidsweek','nos','nrc','sevendays'])
		for key in fm.iterkeys():
			writer.writerow([key] + [d[key] for d in dicts])  


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	main()