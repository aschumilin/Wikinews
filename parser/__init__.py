import xml.etree.ElementTree as ET

#def descend(element):
#	if list(element).__len__()>0:
#		print element.tag
#		descend(element)
#	else:
#		print element.tag

#dump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml")
testdump = ET.parse('/media/MYLINUXLIVE/AIFB/datasets/test_xml.xml')
doc = testdump.getroot()

liste = doc.findall(".//*")
for el in liste:
	print el.tag
		

#elements = list(doc)
#for el in elements:
#	print el.tag 
