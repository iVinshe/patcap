import csv
import os

"""
Hope that you have a jaccard.csv ready on current directory
"""


METHOD = 'jaccard'

def splitter():
	if not os.path.exists(METHOD + '/sorted'):
		os.makedirs(METHOD + '/sorted')
	#try stat is better
	theIndex = csv.writer(open(METHOD + '/index.csv','w'), delimiter = ',')
	allPatents = set()
	similarity = csv.reader(open(METHOD +'.csv'))
	for pair in similarity:
		if pair[0] not in allPatents:
			allPatents.add(pair[0])
			theIndex.writerow([pair[0]])
			temp = open(METHOD + '/sorted/' + pair[0] + '.csv','w') #erase later
			temp.close()
		tempWriter = csv.writer(open(METHOD + '/sorted/' + pair[0] + '.csv','a'))
		tempWriter.writerow(pair)
	

def minorSorter(filename, mainList):
	# check filename type
	minSorter = csv.reader(open(METHOD + '/sorted/' + filename + '.csv','r'), delimiter = ',')
	sortedP = csv.writer(open(METHOD + '/sorted/' + filename + '_S.csv','w'), delimiter = ',')
	ranker = {}
	for pair in minSorter:
		if float(pair[2]) not in ranker:
			ranker[float(pair[2])] = [pair]
		else:
			ranker[float(pair[2])] += [pair]
	theRank = sorted(ranker.keys(), reverse = True)
	numRanker = 1 
	for similarityValue in theRank:
		ranker[similarityValue].sort()
		for sameSim in ranker[similarityValue]:
			sortedP.writerow(sameSim + [numRanker])
			mainList.writerow(sameSim + [numRanker])
		numRanker += len(ranker[similarityValue])
	os.remove(METHOD + '/sorted/' + filename + '.csv')

def mainSorter():
	theIndex = csv.reader(open(METHOD + '/index.csv','r'), delimiter = ',')
	wholeSortedList = csv.writer(open(METHOD + '/' + METHOD + '_s.csv','w'), delimiter = ',')
	for name in theIndex:
		minorSorter(name[0], wholeSortedList)

if __name__=='__main__':
	splitter()
	mainSorter()