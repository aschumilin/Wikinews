""" sort pages by character count in the text element -> sort out the short ones """

import operator
import os
from Timer import Timer
from shutil import copyfile
import traceback


articles_pages = "/dev/shm/wikinews/articles_pages/" # this one must exist
articles_cleaned = "/dev/shm/wikinews/articles_cleaned/" # create this one if needed
if not os.path.exists(articles_cleaned):
    os.makedirs(articles_cleaned)


dir = "/media/MYLINUXLIVE/AIFB/datasets/en/en_stats/" # this one must exist
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
for item in pageCountList:
	pageTextLength = item[1]
	pageFileName = str(item[0])

	if pageTextLength >= cutOffLength:
		# copy file from base dir to the "cleaned" folder
		#os.system(str('cp ' + articles_pages + pageFileName + ' ' + articles_cleaned + pageFileName)) # this doesnt work
		try: 
			copyfile(str(articles_pages + pageFileName), str(articles_cleaned + pageFileName))
		except:
			print "error: ", pageFileName 
			traceback.print_exc()
		

T.click()

print "copying done in ", T.show()
###################
# manually delete:
###################
# 3-Main_Page
# 118215-Main_Page_Lite
# -Australia-2005 ... 2009 (5 pages election results)
# -Colleges_offering_admission_to_displaced_New (4 pages lists)
# 180311-2010_UK_general_election_results
# 54162-2006_U.S._Congressional_Elections
# 8636-Results_of_2005_United_Kingdom_General_Electi


''' example for python regex
import xml.etree.Elem
xml.etree.ElementInclude  xml.etree.ElementPath     xml.etree.ElementTree     
import xml.etree.ElementTree as ET
dump = ET.parse("/dev/shm/wikinews/articles_cleaned/86383-Al_Sharpton_speaks_out_on_race,_rights_and_w")
root = dump.getroot()
text = root.find(".//{http://www.mediawiki.org/xml/export-0.8/}text").text

m = re.search('\[\[(.+?)\]\]', text)
'''

'''
WIKI NAMESPACES

wiki_ns = ['Media',
 'Special',
 'Talk',
 'User',
 'User talk',
 'Wikinews',
 'Wikinews talk',
 'File',
 'File talk',
 'MediaWiki',
 'MediaWiki talk',
 'Template',
 'Template talk',
 'Help',
 'Help talk',
 'Category',
 'Category talk',
 'Thread',
 'Thread talk',
 'Summary',
 'Summary talk',
 'Portal',
 'Portal talk',
 'Comments',
 'Comments talk',
 'Education Program',
 'Education Program talk',
 'Module',
 'Module talk']

# count occurance of namespaces in the dump 
dictNS = dict()
for ns in wiki_ns:
    anz = len(re.findall("\[\[" + ns + "\:(.+?)\]\]", wikinewsDumpXML))
    dictNS.update({ns:anz})



'''

