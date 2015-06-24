# -*- coding: utf-8 -*-
import sys, getopt, argparse, re, urlparse, chardet
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
	# aviAgeDict = {'0':'Adult', '1':'MaartGroep3', '2':'EindGroep3', '3':'NovGroep4', '4':'MaartGroep4', '5':'EindGroep4', '6':'NovGroep5', '7':'MaartGroep5', '8':'EindGroep5', '9':'KerstGroep6'}
	
		for article in content:
			loc = urlparse.urlparse(article['identifier']).netloc
			cat = article['category']
			soup = BS(article['body'])
			bod = soup.get_text()
			# bod = remove_tags(bod)
			print(bod)
			# bod = HP.feed(article['body'])
			# print(html2text(article['body']))
			# body = remove_tags(html2text(article['body']))
			# bod = re.split('\.[\s|\n]|\!+|\?+',body)
			# body = remove_tags(bod)
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
				file = open('database/genresplit/' + loc + '_' + cat,'a')
			except IOError:
				file = open('database/genresplit/' + loc + '_' + cat,'w')
			for line in bod:
				line = line.encode('utf-8').decode('')
				# print(chardet.detect(line))
				file.write(line + '\n\n')
			file.close()
		# print(domains)


def remove_tags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	P_RE = re.compile('<\/p><p>')
	textN = P_RE.sub('\n', text)
	return TAG_RE.sub('', textN)

if __name__ == "__main__":
	# parser = argparse.ArgumentParser()
	# parser.add_argument("-corpus", "--corpus", help="Pickled file", default="articles.pickle")
	# # Name and location of the pickled articles file
	# args = parser.parse_args()
	main()