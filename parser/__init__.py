import xml.etree.ElementTree as ET

# http://docs.python.org/2/library/xml.etree.elementtree.html

wikinewsDump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml")
for child in wikinewsDump:
	print child.tag, child.attrib

