'''
Created on 18.12.2013

@author: pilatus
'''
import os
from Timer import Timer
import xml.etree.ElementTree as ET

defaultNamespace = "{http://www.mediawiki.org/xml/export-0.8/}"

targetDir = "/dev/shm/wikinews/wikiAPITest/"

sourceDir = "/dev/shm/wikinews/articles_cleaned/"

articles = os.listdir(sourceDir)

i = 0
T = Timer()
T.click()
for art in articles:
    root = ET.parse(sourceDir + art).getroot()
    title = root.find(".//" + defaultNamespace + "title").text.replace(" ", "_")
    """print title
    i += 1
    if i>5:
        break"""
T.click()
print T.show()