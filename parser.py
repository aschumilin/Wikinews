import xml.etree.ElementTree as ET

#dump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml")
testdump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/test_xml.xml")
doc = testdump.getroot()

for element in doc:
	print element.tag
