import xml.etree.ElementTree as ET
import time as time 
from string import join

#def descend(element):
#	if list(element).__len__()>0:
#		print element.tag
#		descend(element)
#	else:
#		print element.tag

#dump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml")
#dump = ET.parse('/media/MYLINUXLIVE/AIFB/datasets/test_xml.xml')
start1 = time.time()
dump = ET.parse('../../../en_wikinews_2013-10-30/enwikinews-20131030-pages-articles.xml')
doc = dump.getroot()
end1 = time.time()






start2 = time.time()
liste = doc.findall(".//*")
end2 = time.time()

outputFile = open('../../../en_wikinews_2013-10-30/wikinews-tags.txt', 'w')

for el in liste:
	print el.tag
	result = el.tag, "\n"
	outputFile.writelines(result)

print "time for parsing the dump: ", end1 - start1, " sec"
print "time for collecting all tags: ", end2 - start2, " sec"
		

#elements = list(doc)
#for el in elements:
#	print el.tag 
