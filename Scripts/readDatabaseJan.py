import sys, getopt, argparse, re, pickle, urllib.parse
from html.parser import HTMLParser as HP
import html
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
	# domains = []

	# Body of the function
	# aviAgeDict = {'0':'Adult', '1':'MaartGroep3', '2':'EindGroep3', '3':'NovGroep4', '4':'MaartGroep4', '5':'EindGroep4', '6':'NovGroep5', '7':'MaartGroep5', '8':'EindGroep5', '9':'KerstGroep6'}
	
	for article in content:
		loc = urllib.parse.urlparse(article['identifier']).netloc
		# bod = HP.feed(article['body'])
		body = remove_tags(html.unescape(article['body']))
		bod = re.split('\.[\s|\n]|\!+|\?+',body)
		# body = remove_tags(article['body'])
		# bod = bytes(body, 'utf-8')
		# print(bytes(body,'utf-8'))

		# bod = remove_tags(article['body'])
		# print(type(bod))

		if loc == 'm.bright.nl':
			loc = 'www.bright.nl'
			# bod = bytes(body, 'utf-8')
		elif loc == 'nos.nl':
			loc = 'www.nos.nl'
			# bod = bytes(body, 'utf-8')
		try:
			file = open('database\\' + loc,'a')
		except IOError:
			file = open('database\\' + loc,'w')
		for line in bod:
			file.write(line + '\n\n')
		file.close()
	# print(domains)


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