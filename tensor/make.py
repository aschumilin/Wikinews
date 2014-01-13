# github mnick - Maximilian Nickel
# mData = loadmat("/path/file.mat")

from scipy.io.matlab import loadmat
import codecs, os
from Timer import Timer

T = Timer()

def extractPhrase(entityString):
	
	if ":" in entityString:

		if entityString.startswith(":"):
			# :...:
			pref = entityString.split(":")[1].lower()
			if pref == "w":
				return extractPhrase("w|" + entityString[3:])
			elif pref == "wikipedia":
				return extractPhrase("w|" + entityString[11:])
		else:
			pref = entityString.split(":")[0].lower()
			if pref == "w":
				return extractPhrase("w|" + entityString[2:])
			elif pref == "wikipedia":
				return extractPhrase("w|" + entityString[10:])
				
				
			 
	if "|" in entityString:
		parts = entityString.split("|")
        
		if (parts[0].lower() == "w") or (parts[0].lower() == "wikipedia"):
			if len(parts) == 2:
				# w|ent
				return parts[1].replace(" ", "_"), parts[1]     
				print "detected: (w, wikipedia)|ent"
			elif len(parts) == 3:
				# w|ent|phrase
				return parts[1].replace(" ", "_"), parts[2]
				print "detected: (w, wikipedia)|ent|phrase"
			elif len(parts) ==    4:
				# w|ent|anchor|phrase
				return parts[1].replace(" ", "_"), parts[3]   
				print "detected: (w, wikipedia)|ent|anchor|phrase"   




"""
r = extractPhrase(s)     
if (r == None): print "empty return"   
print '%s ~ %s' % (r[0], r[1])
"""

##########
##########
separator = "\t\t\t\t"
##########
##########


sourceDir = "/dev/shm/wikinews/entities_pruned/"

resultFile = open("/dev/shm/wikinews/entities_phrases.txt", "w")

articles = os.listdir(sourceDir)

T.click()

entCount = 0
goodEnts = 0
for fileName in articles:
	
	article = open(sourceDir + fileName, "r")
	numEntityMentions = 0
#	print "===============", fileName, "======="
	for entity in article:
		entCount += 1
		# count entities in each article
		#print entity
		returned = extractPhrase(entity)
		if returned != None:
			goodEnts += 1
			#print returned[0]
			line = returned[0].strip() + separator + returned[1].strip()
			resultFile.write(line+"\n")
		else:
			print "===============", fileName, "======="
			print "    ", entity


resultFile.close()

T.click()
print "all: ", entCount
print "good: ", goodEnts
print "done in ", T.show()












