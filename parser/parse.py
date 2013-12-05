import xml.etree.ElementTree as ET
from Timer import Timer
import logging
import sys
import os


# some fixed values
#baseDir = "/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/"
baseDir = "/dev/shm/wikinews/" 
elementName = "page"
pageDistinguisher = "ns" # this child element of a page (here: wiki-internal-namespace) separates good articles from rubbish


articleDirName = baseDir + "articles_pages/"
junkDirName = baseDir + "other_pages/"
logFileName = baseDir + "debug.log"
dumpFileName = "/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/enwikinews-20131030-pages-articles.xml"

T = Timer() # stop watch to keep track of cpu time
#===================

handlerDebug = logging.FileHandler(logFileName)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerDebug.setFormatter(formatter)
L = logging.getLogger("wikinews")
L.setLevel(logging.DDEBUG)
L.addHandler(handlerDebug)




# 1 
# parse dump and get the root of xml tree
#
L.debug("parsing started")
T.click()
dump = ET.parse(dumpFileName)
wikinews = dump.getroot()
T.click()
parsingTime = T.show()
L.debug("done parsing in: " + parsingTime)s


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
			
			targetFileName = pageID + "-" + pageTitle.replace(":", "#").replace(" ", "_")
			
			targetFile = None
			if pageNS == 0: 
				# this page is a regular Wikinews article
				# save it appropriately
				print targetFileName
				targetFile = open(articleDirName + targetFileName, "w")
				numRegularArticles += 1
			else:
				# this page is not an article
				# save it to the junk folder
				targetFile = open(junkDirName + targetFileName, "w")
				numOtherPages += 1

			targetFile.write(ET.tostring(page, encoding="utf-8")
			targetFile.close()	
				
		numProcessedPages += 1
	except:
		exceptionOccured = True
		L.debug("failed at page " + targetFileName + "YYY Exception: " + sys.exc_info()[0])
T.click()

pagesProcessingTime = T.show()
L.debug("processing done in " + pagesProcessingTime + ":: 0 = " + str(numProcessedPages - numRegularArticles - numOtherPages))
	

print "dump parsed in ", parsingTime
print "xpath pages in ", traversingTime
print "process & save pages in ", pagesProcessingTime

# 5
# move the final output out of /dev/shm to home dir

if ("/dev/shm" in baseDir) & (not exceptionOccured):
	os.system("cp -r /dev/shm/wikinews/* /home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/")
