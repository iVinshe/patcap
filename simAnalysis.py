import sys
import csv
import numpy
import os

"""
Need to install numpy. 
Use "sudo apt-get install python-numpy"

"""

def citAnalysis(csvFile):
	citList = csv.reader(csvFile)
	fileName = os.path.splitext(csvFile.name)[0]

	simList = []
	rankList = []

	L10 = 0
	L50 = 0
	L100 = 0
	L500 = 0
	L1000 = 0
	Counter = 0
	for row in citList:
		Counter += 1
		simList.append(float(row[5]))
		rankList.append(int(row[4]))
		if int(row[4]) <= 10:
			L10 += 1
			L50 += 1
			L100 += 1
			L500 += 1
			L1000 +=1
		elif int(row[4]) <= 50:
			L50 += 1
			L100 += 1
			L500 += 1
			L1000 +=1
		elif int(row[4]) <= 100:
			L100 += 1
			L500 += 1
			L1000 +=1
		elif int(row[4]) <= 500:
			L500 += 1
			L1000 += 1
		elif int(row[4]) <= 1000:
			L1000 += 1

	Counter = str(Counter)
	minSim = str(numpy.amin(simList))
	minRank = str(numpy.amin(rankList))
	medianSim = str(numpy.median(simList))
	medianRank = str(numpy.median(rankList))
	meanSim = str(numpy.mean(simList))
	meanRank = str(numpy.mean(rankList))
	maxSim = str(numpy.amax(simList))
	maxRank = str(numpy.amax(rankList))
	Q1Sim = str(numpy.percentile(simList, 75))
	Q1Rank = str(numpy.percentile(rankList, 25))
	Q3Sim = str(numpy.percentile(simList, 25))
	Q3Rank = str(numpy.percentile(rankList, 75))
	sdSim = str(numpy.std(simList))
	sdRank = str(numpy.std(rankList))

	ana = csv.writer(open(fileName +'_analysis.csv','w'), delimiter = ',')
	ana.writerow(['Data_point', Counter])
	ana.writerow(['Min_sim', minSim])
	ana.writerow(['Max_Sim', maxSim])
	ana.writerow(['Median_sim', medianSim])
	ana.writerow(['Mean_sim', meanSim])
	ana.writerow(['First_Q_sim', Q1Sim])
	ana.writerow(['Third_Q_sim', Q3Sim])
	ana.writerow(['Standard_Dev_sim', sdSim])
	ana.writerow(['Min_rank', minRank])
	ana.writerow(['Max_rank', maxRank])
	ana.writerow(['Median_rank', medianRank])
	ana.writerow(['Mean_rank', meanRank])
	ana.writerow(['First_Q_rank', Q1Rank])
	ana.writerow(['Third_Q_rank', Q3Rank])
	ana.writerow(['Standard_Dev_rank', sdRank])
	ana.writerow(['Less_than_10', L10])
	ana.writerow(['Less_than_50', L50])
	ana.writerow(['Less_than_100', L100])
	ana.writerow(['Less_than_500', L500])
	ana.writerow(['Less_than_1000', L1000])


if __name__=='__main__':
    if len(sys.argv) == 2:
    	theName = sys.argv[1]
        fileToA = open(theName, 'r')
        citAnalysis(fileToA)
    else:
    	print("""
Input a citation csv file and do analysis on the citations.
An Analysis_filename.txt will be the output.
""")