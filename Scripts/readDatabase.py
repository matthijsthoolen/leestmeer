from collections import Counter
import sys, getopt, argparse, re, pickle

def main(corpus):
	contents = pickle.load(open('articles.pickle', mode='rb'))
	# print(contents)
	# for article in contents:
	# 	print(article)
	# for identifier, identifierC, category, categoryC, title, titleC, body, bodyC in contents:
		# print(identifier)
	for identifier, category, title, body in contents:
		print('identifier')
		for ident,identC in identifier:
			print(ident + ': ' + identC)



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="Textfile of corpus", default="input.txt")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.corpus)