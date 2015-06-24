from collections import Counter
import sys, argparse, re, math, csv
import cPickle as pickle
import ast

def main():
	fm = pickle.load(open('database/3fm_POS_nGrams', 'rb'))
	threesixty = pickle.load(open('database/360_POS_nGrams', 'rb'))
	bright = pickle.load(open('database/bright_POS_nGrams', 'rb'))
	kidsweek = pickle.load(open('database/kidsweek_POS_nGrams', 'rb'))
	nos = pickle.load(open('database/nos_POS_nGrams', 'rb'))
	nrc = pickle.load(open('database/nrc_POS_nGrams', 'rb'))
	sevendays = pickle.load(open('database/sevendays_POS_nGrams', 'rb'))
	# P = fm, threesixty, bright, kidsweek, nos, nrc, sevendays
	List = [(fm,'3fm_POS_nGrams'), (threesixty, '360_POS_nGrams'), (bright, 'bright_POS_nGrams'), (kidsweek, 'kidsweek_POS_nGrams'), (nos, 'nos_POS_nGrams'), (nrc, 'nrc_POS_nGrams'), (sevendays, 'sevendays_POS_nGrams')]
	union = Counter(list(fm + threesixty + bright + kidsweek + nos + nrc + sevendays))
	# for x in union.keys():
		# for source,name in List:
		# 	source.update(x=0)
	# print(fm)
	fm.update(union)
	threesixty.update(union)
	bright.update(union)
	kidsweek.update(union)
	nos.update(union)
	nrc.update(union)
	sevendays.update(union)
	# print(union)

	fm.subtract(union)
	threesixty.subtract(union)
	bright.subtract(union)
	kidsweek.subtract(union)
	nos.subtract(union)
	nrc.subtract(union)
	sevendays.subtract(union)
	# print(str(len(fm)) + ' ' + str(len(nos)))
	print(fm['Pron Pron Adv'])

	dicts = [fm,threesixty,bright,kidsweek,nos,nrc,sevendays]
	# print(type(fm))

	with open('POS_nGrams.csv', 'wb') as g:
		writer = csv.writer(g, delimiter='\t')
		writer.writerow(['ID', '3fm', '360magazine', 'bright', 'kidsweek','nos','nrc','sevendays'])
		for key in fm.iterkeys():
			writer.writerow([key] + [d[key] for d in dicts])  
	# 	w = csv.DictWriter(g, union.keys())
	# 	w.writeheader()
	# 	w.writerow(P)


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	# parser = argparse.ArgumentParser()
	# parser.add_argument("-corpus", "--corpus", help="File of corpus")
	# # parser.add_argument("-text", "--text", help="Text as string")
	# #Name and location of the text file to be parsed
	# args = parser.parse_args()
	main()