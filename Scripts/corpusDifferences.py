import textDifference, argparse, sys
import textDifference
from collections import Counter


def main(paragraph):
	print('3fm score:')
	textDifference.main('database/3fm_POS_nGrams_idf',paragraph)

	print('360 score:')
	textDifference.main('database/360_POS_nGrams_idf',paragraph)

	print('bright score:')
	textDifference.main('database/bright_POS_nGrams_idf',paragraph)

	print('kidsweek score:')
	textDifference.main('database/kidsweek_POS_nGrams_idf',paragraph)

	print('nos score:')
	textDifference.main('database/nos_POS_nGrams_idf',paragraph)

	print('nrc score:')
	textDifference.main('database/nrc_POS_nGrams_idf',paragraph)

	print('sevendays score:')
	textDifference.main('database/sevendays_POS_nGrams_idf',paragraph)


# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="File of corpus")
	# parser.add_argument("-text", "--text", help="Text as string")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.corpus)
