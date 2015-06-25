# -*- coding: utf-8 -*-
import sys, getopt, re, urlparse, chardet
from bs4 import BeautifulSoup as BS
import cPickle as pickle
import AVIscoreMod

def main():
	# Opens the pickled file as 'content'. This is a dictionary of features
	# of every article:
	# 1. identifier (source of the article)
	# 2. category   (type of the article)
	# 3. title      (title of the article)
	# 4. body       (body of the article)
	# All of these can be accessed like this:
	# 'dictionary name'['feature name']
	with open('articles.pickle', mode='rb') as f:
		content = pickle.load(f)

	# Here the empty variables and their types should be defined
	# e.g.: domains = []
	# domains = []

	# Body of the function	
		for article in content:
			loc = urlparse.urlparse(article['identifier']).netloc
			cat = article['category']
			soup = BS(article['body'])
			bod = soup.get_text()

			if loc == 'm.bright.nl':
				loc = 'www.bright.nl'
			elif loc == 'nos.nl':
				loc = 'www.nos.nl'
			try:
				file = open('database/genresplit/' + loc + '_' + cat,'a')
			except IOError:
				file = open('database/genresplit/' + loc + '_' + cat,'w')
			for line in bod:
				line = line.encode('utf-8').decode('')
				file.write(line + '\n\n')
			file.close()

# Removes erroneous HTML tags
def remove_tags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	P_RE = re.compile('<\/p><p>')
	textN = P_RE.sub('\n', text)
	return TAG_RE.sub('', textN)

if __name__ == "__main__":
	main()