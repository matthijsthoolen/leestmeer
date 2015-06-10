import sys, getopt, argparse, re, pickle, urllib.parse
import xml.etree.ElementTree as ET
import AVIscoreMod

def main(corpus):
	# Opens the pickled file as 'content'. This is a dictionary of features
	# of every article:
	# 1. identifier (source of the article)
	# 2. category   (type of the article)
	# 3. title      (title of the article)
	# 4. body       (body of the article)
	# All of these can be accessed like this:
	# 'dictionary name'['feature name']
	content = pickle.load(open('articles.pickle', mode='rb'))

	# Here the empty variables and their types should be defined
	# e.g.: domains = []
	domains = []

	# Body of the function
	file = open('articles.txt','w')
	for article in content:
		loc = urllib.parse.urlparse(article['identifier']).netloc
		if domains.count(loc) == 0:
			domains.append(loc)
		# print(article['body'])
		bod = remove_tags(article['body'])
		file.write('AVI score: ' + str(AVIscoreMod.main(bod,'avi','text')))
		file.write('\n')
		file.write(bod)
		file.write('\n ----------------------- \n')

def remove_tags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	P_RE = re.compile('<\/p><p>')
	textN = P_RE.sub('\n', text)
	return TAG_RE.sub('', textN)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-corpus", "--corpus", help="Pickled file", default="articles.pickle")
	# Name and location of the pickled articles file
	args = parser.parse_args()
	main(args.corpus)