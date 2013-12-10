""" sort pages by character count in the text element """

import operator
import os
from Timer import Timer
from shutil import copyfile
import traceback


articles_cleaned = "/dev/shm/wikinews/articles_cleaned/"
articles_pages = "/dev/shm/wikinews/articles_pages/"

dir = "/media/MYLINUXLIVE/AIFB/datasets/en/"
file = open(dir + "charCount", "r")
resultFile = open(dir + "pagesSortedByCount", "w")
charCountStat = open(dir + "charCountStatistics", "w")



# build dictionary of page name - char count in page text
rawDict = dict()

for line in file:
	pageName = line.split(" ")[0]
	charCount = int(line.split(" ")[2])
	rawDict.update({pageName: charCount})

print charCount.__class__()

# sort dictionary
T = Timer()
T.click()
#sorts dict by second element of item - RETURNS A SORTED LIST of items
# if list is put into a dict, then ORDERING IS LOST !!!
pageCountList = sorted(rawDict.iteritems(), key = operator.itemgetter(1)) 
T.click()
print "time to sort 37501 items: " ,T.show()


# write the files
for item in pageCountList:
	resultFile.write(item[0] + " " + str(item[1]) + "\n")
	charCountStat.write(str(item[1]) + "\n")
		
resultFile.close()
charCountStat.close()



#############
## Remove junk
#############
print "start copying good articles"
cutOffLength = 510 # characters
T.click()
i = 0
for item in pageCountList:
	pageTextLength = item[1]
	pageFileName = str(item[0])

	if pageTextLength >= cutOffLength:
		# copy file from base dir to the "cleaned" folder
		#os.system(str('cp ' + articles_pages + pageFileName + ' ' + articles_cleaned + pageFileName)) # this doesnt work
		try: 
			copyfile(str(articles_pages + pageFileName), str(articles_cleaned + pageFileName))
			i += 1 
			if (i % 100) == 0:
				print ".",
		except:
			print "error: ", pageFileName 
			traceback.print_exc()
		

T.click()

print "copying done in ", T.show()
