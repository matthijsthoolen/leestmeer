import POStagger_corpus as POStagger
import ngramProfilerFiles as ngramProfiler
import sys

def main():
	#print("hallo1")
	POStagger.main('database/www.kidsweek.nl','database/kidsweek_POS')
	loadShit(0)
	POStagger.main('database/www.nos.nl','database/nos_POS')
	loadShit(1)
	POStagger.main('database/www.sevendays.nl','database/sevendays_POS')
	loadShit(2)
	POStagger.main('database/www.bright.nl','database/bright_POS')
	loadShit(3)
	POStagger.main('database/www.nrc.nl','database/nrc_POS')
	loadShit(4)
	POStagger.main('database/www.politie.nl','database/politie_POS')
	loadShit(5)
	POStagger.main('database/www.3fm.nl','database/3fm_POS')
	loadShit(6)
	POStagger.main('database/www.360magazine.nl','database/360_POS')
	loadShit(7)
	#POStagger.main('database/test','database/test_POS')
	ngramProfiler.main('database/kidsweek_POS',3)
	loadShit(8)
	ngramProfiler.main('database/nos_POS',3)
	loadShit(9)
	ngramProfiler.main('database/sevendays_POS',3)
	loadShit(10)
	ngramProfiler.main('database/bright_POS',3)
	loadShit(11)
	ngramProfiler.main('database/nrc_POS',3)
	loadShit(12)
	ngramProfiler.main('database/politie_POS',3)
	loadShit(13)
	ngramProfiler.main('database/3fm_POS',3)
	loadShit(14)
	ngramProfiler.main('database/360_POS',3)
	loadShit(15)


animation_strings = (	'[=              ]', 
						'[==             ]', 
						'[===            ]', 
						'[====           ]', 
						'[=====          ]',
                     	'[======         ]', 
                     	'[=======        ]', 
                     	'[========       ]', 
                     	'[=========      ]',
                     	'[==========     ]', 
                     	'[===========    ]', 
                     	'[============   ]', 
                     	'[=============  ]',
                     	'[============== ]', 
                     	'[===============]',
                     	'[====D-O-N-E====]\n')

def loadShit(index):
	sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
	sys.stdout.write(animation_strings[index % len(animation_strings)])
	sys.stdout.flush()

