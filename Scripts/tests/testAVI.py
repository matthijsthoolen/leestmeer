from collections import Counter
import sys, getopt, argparse, re, math, os


def main(testset):
	try:
		file = open(testset, encoding='utf-8', mode='r')
		text = file.read()
		#text = text.replace('\n',' ').replace('\"','')
		# text = text.replace('\.\n','\. ').replace('\n','')
		file.close()	
	except IOError:	
		print('Cannot open '+corpus)
		sys.exit()

	tests = re.split('\n', text)

	for test in tests:
		# print(sentence)
		if (test.find('#') == -1):
			#print(test)
			values = re.split('\s+', test)
			print("Test "+ values[0] +" True AVI score:  "+ values[3])
			os.system("c:\python34\python .\..\AVIscore.py --corpus sentences\\"+ values[0] +".txt")

			
# This function states the commandline arguments that are needed
# for the program to run.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-testset", "--testset", help="Textfile of tests", default="input.txt")
	#Name and location of the text file to be parsed
	args = parser.parse_args()
	main(args.testset)