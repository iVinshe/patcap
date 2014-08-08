import sys
import csv
import os
import bisect



def tagSeek(inputTag):
	seeking = csv.reader(open(inputTag, 'rU'), delimiter = ',')
	tagsIn = []
	for t in seeking:
		bisect.insort(tagsIn, t[0])

	base = csv.reader(open('tags.csv', 'rb'), delimiter = ',')
	outFile = csv.writer(open(os.path.splitext(inputTag)[0] +'_WT.csv','w'), delimiter = ',')

	for tag in base:
		if tag[0] in tagsIn:
			tagsIn.remove(tag[0])
			outFile.writerow(tag)
		if len(tagsIn) == 0:
			break

	if len(tagsIn) > 0:
		print "Cannot find tags for following patents, or there exist duplicate IDs."
		for i in tagsIn:
			print i

if __name__=='__main__':
    if len(sys.argv) == 2:
    	tagIn = sys.argv[1]
        tagSeek(tagIn)
    else:
    	print("""
Input a patent csv file and seek tags in tags.csv.
""")

