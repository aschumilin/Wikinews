import xml.etree.ElementTree as ET
import os
from Timer import Timer

T = Timer()

files = os.listdir("/dev/shm/wikinews/articles_pages/") 


resultFile = open("/dev/shm/wikinews/" + "hasTextElement", "w")
i = 0
j = 0
ctl = 0
T.click()

for fName in files:
	dump = ET.parse("/dev/shm/wikinews/articles_pages/" + fName)
	root = dump.getroot() 
	textEls = root.findall(".//{http://www.mediawiki.org/xml/export-0.8/}text")   
	if len(list(textEls))>0:
		print ".",
		i += 1
		textLength = len(textEls[0].text)
		ctl += textLength
		resultFile.write(fName + " 1 " + str(textLength) + "\n")
	else:
		print "-",
		j += 1
		resultFile.write(fName + " 0 0 \n")

T.click()

resultFile.write("pages with text: " + str(i) + "\n")
resultFile.write("mean text length: " + str(ctl/i)+ "\n")
resultFile.write("pages without text: " + str(j)+ "\n")
resultFile.write("processed in : " + T.show() + "\n")
resultFile.close()



"""for f in files:
	anf = f.split("-")[0]
	try: 
		i = int(anf)
		print f
	except:
		print "bad file:  " , f

"""
