import csv
import mysql.connector
from tempfile import NamedTemporaryFile
import shutil
import os


"""
UTF-8 issue noted

need to install mysql client for python

on terminal:
sudo apt-get install mysql-client

then for python:
http://dev.mysql.com/doc/connector-python/en/connector-python-installation.html

"""

CURR_PATH = 'jaccard'
SQL_USER = 'uspto'
SQL_PASS = 'ferrisbueller'
SQL_HOST = '169.229.7.251'
SQL_DB = 'uspto'

def mainChecker():
	theIndex = csv.reader(open(CURR_PATH + '/index.csv', 'r'))
	cnx = mysql.connector.connect(user = SQL_USER, password = SQL_PASS,host = SQL_HOST,database = SQL_DB)
	cursor = cnx.cursor()

	if not os.path.exists(CURR_PATH + '/sorted'):
		print "Sorted file does not exist!"
		return 0

	if not os.path.exists(CURR_PATH + '/prior'):
		os.makedirs(CURR_PATH + '/prior')
	
	for patent in theIndex:
		minChecker(patent[0], cursor)

def minChecker(p_id, sqlCursor):
	#check PID type
	rank_checker = {}
	theRank = csv.reader(open(CURR_PATH + '/sorted/' + p_id + '_S.csv','r'))
	zeroSimiRank = 0
	zeroSimi = 1.0
	counter = 0
	Found = False
	for row in theRank:
		rank_checker[row[1]] = (row[2] ,row[3])

		if not Found:
			if float(row[2]) == 0.0:
				zeroSimiRank = row[3]
			elif float(row[2]) < float(zeroSimi):
				zeroSimiRank = row[3]
				zeroSimi = row[2]
				counter = 1
			else:
				counter += 1

	if not Found:
		zeroSimiRank = counter + int(zeroSimiRank)

	citedList = csv.writer(open(CURR_PATH + '/prior/' + p_id + '_C_uns.csv','w'), delimiter = ',')

	queryForFuture = 'select citation_id, category from uspatentcitation where patent_id = "' + p_id + '";'
	sqlCursor.execute(queryForFuture)
	isPrior = True
	for (cit_id, category) in sqlCursor:
		citedByExaminer = category == 'cited by examiner'
		pairRank = zeroSimiRank
		simi = 0.0
		if cit_id in rank_checker:
			pairRank = rank_checker[cit_id][1]
			simi = rank_checker[cit_id][0]
		citedList.writerow([p_id, cit_id, isPrior, citedByExaminer, pairRank, simi])


	queryForPast = 'select patent_id, category from uspatentcitation where citation_id = "' + p_id + '";'
	sqlCursor.execute(queryForPast)
	isPrior = False
	for (citBy_id, category) in sqlCursor:
		citedByExaminer = category == 'cited by examiner'
		pairRank = zeroSimiRank
		simi = 0.0
		if citBy_id in rank_checker:
			pairRank = rank_checker[citBy_id][1]
			simi = rank_checker[citBy_id][0]
		citedList.writerow([p_id, citBy_id, isPrior, citedByExaminer, pairRank, simi])

def sortAndAppend():
	theIndex = csv.reader(open(CURR_PATH + '/index.csv', 'r'))
	wholeCitedList = csv.writer(open(CURR_PATH + '/' + CURR_PATH + '_C.csv','w'), delimiter = ',')
	for patent in theIndex:
		sortRankId(patent[0], wholeCitedList)
		os.remove(CURR_PATH + '/prior/' + patent[0] + '_C_uns.csv')



def sortRankId(p_id, mainList):
	unsorted = csv.reader(open(CURR_PATH + '/prior/' + p_id + '_C_uns.csv','r'))
	rankDic = {}

	for row in unsorted:
		if float(row[5]) not in rankDic:
			rankDic[float(row[5])] = [row]
		else:
			rankDic[float(row[5])] += [row]
	# check if we really need this 
	for row in unsorted:
		rankDic[float(row[5])].sort()

	sortedCitedList = csv.writer(open(CURR_PATH + '/prior/' + p_id + '_C.csv','w'), delimiter = ',')
	# in 2.7, the keys are already sorted. Need to verify this property in other version!
	for sim in sorted(rankDic.keys(), reverse = True):
		for sameSim in rankDic[sim]:
			sortedCitedList.writerow(sameSim)
			mainList.writerow(sameSim)






if __name__=='__main__':
	mainChecker()
	sortAndAppend()