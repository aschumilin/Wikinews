""" gettting the entities for each document 
/media/MYLINUXLIVE/AIFB/Wikinews/parser/filter4.py"""

import os, codecs 
from Timer import Timer 

T = Timer()

langPrefixes = ['en', 'de', 'fr', 'nl', 'it', 'es', 'ru', 'sv', 'pl', 'ja', 'pt', 'ar', 'zh', 'uk', 'ca', 'no', 'fi', 'cs', 'hu', 'tr', 'ro', 'sw', 'ko', 'kk', 'vi', 'da', 'eo', 'sr', 'id', 'lt', 'vo', 'sk', 'he', 'fa', 'bg', 'sl', 'eu', 'war', 'lmo', 'et', 'hr', 'new', 'te', 'nn', 'th', 'gl', 'el', 'ceb', 'simple', 'ms', 'ht', 'bs', 'bpy', 'lb', 'ka', 'is', 'sq', 'la', 'br', 'hi', 'az', 'bn', 'mk', 'mr', 'sh', 'tl', 'cy', 'io', 'pms', 'lv', 'ta', 'su', 'oc', 'jv', 'nap', 'nds', 'scn', 'be', 'ast', 'ku', 'wa', 'af', 'be-x-old', 'an', 'ksh', 'szl', 'fy', 'frr', 'yue', 'ur', 'ia', 'ga', 'yi', 'als', 'hy', 'am', 'roa-rup', 'map-bms', 'bh', 'co', 'cv', 'dv', 'nds-nl', 'fo', 'fur', 'glk', 'gu', 'ilo', 'kn', 'pam', 'csb', 'km', 'lij', 'li', 'ml', 'gv', 'mi', 'mt', 'nah', 'ne', 'nrm', 'se', 'nov', 'qu', 'os', 'pi', 'pag', 'ps', 'pdc', 'rm', 'bat-smg', 'sa', 'gd', 'sco', 'sc', 'si', 'tg', 'roa-tara', 'tt', 'to', 'tk', 'hsb', 'uz', 'vec', 'fiu-vro', 'wuu', 'vls', 'yo', 'diq', 'zh-min-nan', 'zh-classical', 'frp', 'lad', 'bar', 'bcl', 'kw', 'mn', 'haw', 'ang', 'ln', 'ie', 'wo', 'tpi', 'ty', 'crh', 'jbo', 'ay', 'zea', 'eml', 'ky', 'ig', 'or', 'mg', 'cbk-zam', 'kg', 'arc', 'rmy', 'gn', 'so', 'kab', 'ks', 'stq', 'ce', 'udm', 'mzn', 'pap', 'cu', 'sah', 'tet', 'sd', 'lo', 'ba', 'pnb', 'iu', 'na', 'got', 'bo', 'dsb', 'chr', 'cdo', 'hak', 'om', 'my', 'sm', 'ee', 'pcd', 'ug', 'as', 'ti', 'av', 'bm', 'zu', 'pnt', 'nv', 'cr', 'pih', 'ss', 've', 'bi', 'rw', 'ch', 'arz', 'xh', 'kl', 'ik', 'bug', 'dz', 'ts', 'tn', 'kv', 'tum', 'xal', 'st', 'tw', 'bxr', 'ak', 'ab', 'ny', 'fj', 'lbe', 'ki', 'za', 'ff', 'lg', 'sn', 'ha', 'sg', 'ii', 'cho', 'rn', 'mh', 'chy', 'ng', 'kj', 'ho', 'mus', 'kr', 'hz', 'mwl', 'pa', 'xmf', 'lez', 'chm']

wikiPrefixes = ['w', 'wikipedia']



sourceDir = "/dev/shm/wikinews/candidates_good/"
resultLangDir = "/dev/shm/wikinews/lang_links/"
resultEntDir = "/dev/shm/wikinews/entities/"
if not os.path.exists(resultLangDir):
    os.makedirs(resultLangDir)
if not os.path.exists(resultEntDir):
    os.makedirs(resultEntDir)


articles = os.listdir(sourceDir) 

langLinkStat=[] # number of lang links per article
entStat = [] # number of ents per article


globalLangLinks = codecs.open("/dev/shm/wikinews/globalLangLinks", "w", "utf-8")
globalEnts = codecs.open("/dev/shm/wikinews/globalEnts", "w", "utf-8")

langLinkStatFile = open("/dev/shm/wikinews/llStat", "w")
langLinkStatArray = dict()
entStatFile = open ("/dev/shm/wikinews/entStat", "w")

#strangePrefixes = codecs.open("/dev/shm/wikinews/strangePrefixes", "w", "utf-8")
#goodPrefixes = codecs.open("/dev/shm/wikinews/goodPrefixes", "w", "utf-8")

T.click()
for fileName in articles:
	
	numLl = 0
	numEnt = 0
	
	resultLangFile = codecs.open(resultLangDir + fileName, "w", "utf-8")
	resultEntFile = codecs.open(resultEntDir + fileName, "w", "utf-8")
	
	# iterate over each article's candidate file and decide whether entry is lang-link or entity
	sourceFile = codecs.open(sourceDir + fileName, "r", "utf-8")

	for line in sourceFile:
		line = line.encode("utf-8").decode("utf-8") # !!!! read as UTF-8
		langPref = line.split(":")[0]
		


		if langPref in langPrefixes:
			# candidate is a lang link
			try:
				numLl += 1
				resultLangFile.write(line)
				globalLangLinks.write(line)
				if langLinkStatArray.get(langPref) == None:
					langLinkStatArray.update({langPref: 1})
				else:
					langLinkStatArray.update({langPref: langLinkStatArray.get(langPref)+1})
			except:
				print "ll ERROR ", line
		else:
			# candidate is an entity
			try:
				numEnt += 1
				resultEntFile.write(line)
				globalEnts.write(line)
			except:
				print "ent ERROR ", line
			
			
	resultLangFile.close()
	resultEntFile.close()
	
	# update statistics
	langLinkStat.append(numLl)
	entStat.append(numEnt)


# write stats to files
for i in langLinkStat:
	langLinkStatFile.write(str(i) + "\n")
for j in entStat:
	entStatFile.write(str(j) + "\n")


globalLangLinks.close()
globalEnts.close()
	

T.click()
print " lang links: ", str(summe(langLinkStat)), "\n entities: ", str(summe(entStat))
print "done in " , T.show()


# calculating entity and langlink stats
e = dict()
for j in entStat:
	if e.get(j) == None:
		e.update({j: 1})
	else:
		oldNum = e.get(j)
		e.update({j: oldNum+1})
print e
print "--------------------------------"
l = dict()
for i in langLinkStat:
	if l.get(i) == None:
		l.update({i: 1})
	else:
		oldNum = l.get(i)
		l.update({i: oldNum+1})
print l
print "--------------------------------"
print langLinkStatArray
########## 
