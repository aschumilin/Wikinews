import xml.etree.ElementTree as ET
from Timer import Timer
import logging
import sys
import os
import traceback


# some fixed values

elementName = "page"
pageDistinguisher = "ns" # this child element of a page (here: wiki-internal-namespace) separates good articles from rubbish
T = Timer() # stop watch to keep track of cpu time

#baseDir = "/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/"
baseDir = "/dev/shm/wikinews/" 

#homeDir =  "/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/"
homeDir = "/media/MYLINUXLIVE/AIFB/datasets/en/"

#dumpFileName = "/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/enwikinews-20131030-pages-articles.xml"
dumpFileName = "/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml"

articleDirName = baseDir + "articles_pages/"
junkDirName = baseDir + "other_pages/"
logFileName = baseDir + "debug.log"



#===================


handlerDebug = logging.FileHandler(logFileName)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerDebug.setFormatter(formatter)
L = logging.getLogger("wikinews")
L.setLevel(logging.DEBUG)
L.addHandler(handlerDebug)

# 0
# check if necessery dirs exist
#
if not os.path.exists(articleDirName):
	L.debug("clean-article directory missing at " + articleDirName)
	os.system("mkdir " + articleDirName)	
	#sys.exit()
if not os.path.exists(junkDirName):
	L.debug("junk-page directory missing at " + junkDirName)
	os.system("mkdir " + junkDirName)	
	#sys.exit()
if not os.path.exists(baseDir):
	print "base directory missing at ", baseDir, "\n ...exiting script..."
	sys.exit()




# 1 
# parse dump and get the root of xml tree
#
L.debug("==============================================")
L.debug("==============================================")
L.debug("parsing started")
T.click()
dump = ET.parse(dumpFileName)
wikinews = dump.getroot()
T.click()
parsingTime = T.show()
L.debug("done parsing in: " + parsingTime)


# 2 
# extract the namespace string from the root element tag name
# should be "{http://www.mediawiki.org/xml/export-0.8/}"
#
namespace = wikinews.tag.split("}")[0].strip() + "}"


# 3
# collect all target elements from the xml tree
#
L.debug("xpathing all elements of interest")
T.click()
pages = wikinews.findall(".//" + namespace + elementName)
T.click()
traversingTime = T.show()
L.debug("done xpathing in: " + traversingTime)



# 4
# write elements to individual files
# filter regular articles from other pages
#
L.debug("processing pages...")
T.click()

numProcessedPages = 0
numRegularArticles = 0
numOtherPages = 0
exceptionOccured = False

for page in pages:
	try:
		if len(list(page)) > 1: # page must have child elements!
			# if page.find(".//" + namespace + distinguisherName) != None:
			
			# use id and title as filename
			pageNS = int(page.find(".//" + namespace + pageDistinguisher).text)
			pageTitle = page.find(".//" + namespace + "title").text
			pageID = page.find(".//" + namespace + "id").text
			
			fullName = pageID + "-" + pageTitle.replace(" ", "_").replace(":", "#").replace("/", "-")
			targetFileName = fullName[0:50]
			# first replace: title blanks / second: wiki-namespace colons / third: wiki-pages special chars 

			print "tfn: " , 
			

			if pageNS == 0: 
				# this page is a regular Wikinews article
				# save it appropriately
				print targetFileName
				targetFile = open(articleDirName + targetFileName, "w")
				targetFile.write(ET.tostring(page, encoding="utf-8"))
				targetFile.close()
				numRegularArticles += 1
			else:
				# this page is not an article
				# save it to the junk folder
				targetFile = open(junkDirName + targetFileName, "w")
				targetFile.write(ET.tostring(page, encoding="utf-8"))
				targetFile.close()
				numOtherPages += 1

				
				
		numProcessedPages += 1
	except:
		exceptionOccured = True
		L.debug("failed at " + targetFileName + " === Exception: " + str(sys.exc_info()[0]))
		print "=== failed at page " , targetFileName , " === Exception: " , str(sys.exc_info()[0])
		traceback.print_exc()
T.click()

pagesProcessingTime = T.show()
L.debug("processing done in " + pagesProcessingTime + " :: " + str(numRegularArticles) + " 0-wiki-namespace articles found")
	

print "dump parsed in ", parsingTime
print "xpath pages in ", traversingTime
print "process & save pages in ", pagesProcessingTime
if exceptionOccured: print "es gab eine Exception bei page processing"

# 5
# move the final output out of /dev/shm to home dir

T.click()
if ("/dev/shm" in baseDir): # if all work was done in temp memory, copy results home

	# better: compress results:
	L.debug("start compression of baseDir  " + homeDir)
	os.system("tar -zcvf " + baseDir + "wikinews-pages.tar.gz " + daseDir)
	#os.system("cp -r /dev/shm/wikinews/* " + homeDir)
T.click()
L.debug("copying done in " + T.show())




