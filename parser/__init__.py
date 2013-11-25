import xml.etree.ElementTree as ET

wikinewsDump = ET.parse("wikinews source xml")
for child in wikinewsDump:
	print child.tag, child.attrib
# http://docs.python.org/2/library/xml.etree.elementtree.html
