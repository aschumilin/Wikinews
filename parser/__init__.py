import xml.etree.ElementTree as ET

wikinewsDump = ET.parse("/media/MYLINUXLIVE/AIFB/datasets/en/enwikinews-20131030-pages-articles.xml")
for child in wikinewsDump:
	print child.tag, child.attrib
# http://docs.python.org/2/library/xml.etree.elementtree.html
