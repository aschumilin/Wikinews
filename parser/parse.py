import xml.etree.ElementTree as ET
from Timer import Timer
import logging

handlerDebug = logging.FileHandler('./log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerDebug.setFormatter(formatter)
L = logging.getLogger("wikinews")
L.setLevel(logging.DDEBUG)
L.addHandler(handlerDebug)

T = Timer()


#def descend(element):
#	if list(element).__len__()>0:
#		print element.tag
#		descend(element)
#	else:
#		print element.tag

#dump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml")
#dump = ET.parse('/media/MYLINUXLIVE/AIFB/datasets/test_xml.xml')
#dump = ET.parse('../../../en_wikinews_2013-10-30/enwikinews-20131030-pages-articles.xml')


# 1 
# parse dump and get the root of xml tree
L.debug("parsing started")
T.click()
dump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml")
wikinews = dump.getroot()
T.click()
parsingTime = T.show()
L.debug("done parsing in: " + parsingTime)


# 2 
# extract the namespace string from the root element tag name
namespace = wikinews.tag.split("}")[0].strip() + "}"


# 3
#
L.debug("xpathing all page elements")
T.click()
liste = wikinews.findall(".//*")
T.click()
traversingTime = T.show()
L.debug("done xpathing pagen in: " + traversingTime)


#for el in liste:
#	print el.tag
#	result = el.tag, "\n"
#	outputFile.writelines(result)

print "time for parsing the dump: ", parsingTime
print "time for collecting all page elements: ", traversingTime
		

#elements = list(doc)
#for el in elements:
#	print el.tag 
