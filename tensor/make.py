""" 
extract the pure entity names and separate the phrases. Do additional cleaning:
e.g. entity: _Angela_Merkel = _Angela_Merkel_ = Angela_Merkel = angela_merkel
e.g. phrase: "Forbes Magazine" = "Forbes" magazine
"""

# tensor factorization: github mnick - Maximilian Nickel
# mData = loadmat("/path/file.mat")

from scipy.io.matlab import loadmat
import os, sys, csv, json
from Timer import Timer


T = Timer()

def extractPhrase(entityString):
	
	if ":" in entityString:

		if entityString.startswith(":"):
			# ":w/wikipedia:"
			pref = entityString.split(":")[1].lower()
			if pref == "w":
				return extractPhrase("w|" + entityString[3:])
			elif pref == "wikipedia":
				return extractPhrase("w|" + entityString[11:])
		else:
			# "w/wikipedia:"
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
			elif len(parts) ==	4:
				# w|ent|anchor|phrase
				return parts[1].replace(" ", "_"), parts[3]   
				print "detected: (w, wikipedia)|ent|anchor|phrase"   


##########
##########
separator = "\t\t\t\t"
##########
##########

T.click()
# 1.  build up dictionaries of entities and phrases 
#============================================
#============================================

sourceDir = "/dev/shm/wikinews/entities_pruned/"
resultFile = open("/dev/shm/wikinews/entities_phrases.txt", "w")

resultEntDictFile = "/dev/shm/wikinews/ent_dict.json"
resultPhraseDictFile = "/dev/shm/wikinews/phrase_dict.json"
resultDocDictFile = "/dev/shm/wikinews/doc_dict.json"

articles = os.listdir(sourceDir)


entDict = dict()
phraseDict = dict()
entCount = 0
docCount = 0

docIndex = 0
entIndex = 0
phraseIndex = 0

for fileName in articles:
	
	article = open(sourceDir + fileName, "r")
	numEntityMentions = 0	
		
	for entity in article:
		returned = extractPhrase(entity)
		if returned != None:
			
			
			#resultFile.write(returned[0].strip() + separator + returned[1].strip() + "\n") # print all entitiy mentions and their phrases to file
			
			entCount += 1
			ent = returned[0].strip()
			phrase = returned[1].strip()
			
			
			#########
			#########
			# clean entities and 
			# 1. cut off a leading underscore
			if ent == "":
				print fileName, ": ", entity
				continue # avoid broken entity mentions
			
			if ent[0] == "_":
				ent = ent[1:] 
				
			# 2. cut off trailing underscore
			if ent[len(ent)-1] == "_":
				ent = ent[:len(ent)-1] 
				
			# 3. transfer to lower case and strip blanks
			ent = ent.lower().strip()
			
			# 4. remove all " from phrases
			phrase = phrase.replace("\"", "")
					
						
			#########
			#########
			# check if entity and phrase is already in the list
			# if not, add it and increment the index
			if ent not in entDict:
				entDict.update({ ent : entIndex})
				entIndex += 1
			
			if phrase not in phraseDict:
				phraseDict.update({ phrase : phraseIndex })
				phraseIndex += 1
			#=========================================	
			
		else:
			print "===============", fileName, "======="
			print "	returned = None: bad Entity mention: ", entity


resultFile.close()

T.click()

print "=== SUMMARY ==="
print "dictionaries building done in ", T.show()
print "found ", entCount, " entity mentions in ", len(articles), " articles"
print " number of distinct entities: ", len(entDict)
print " referred to by ", len(phraseDict), " distinct phrases"

print " ", len(articles), " ", len(entDict), " ", len(phraseDict), " ", entCount

"""
=== SUMMARY (entity mention threshold=3) ===
dictionaries building done in  0.967303037643s
found  161717  entity mentions in  15720  articles
 number of distinct entities:  64310
 referred to by  69850  distinct phrases


=== SUMMARY (entity mention threshold=5) ===
dictionaries building done in  1.01186704636s
found  149496  entity mentions in  12243  articles
 number of distinct entities:  60839
 referred to by  65920  distinct phrases
"""
# tf = open("/dev/shm/wikinews/DE.txt", "w")
# for e in entDict:
#	 tf.write(e + "\n")
# tf.close()
# tf = open("/dev/shm/wikinews/DP.txt", "w")
# for p in phraseDict:
#	 tf.write(p+"\n")
# tf.close()

#print "docDict: ", sys.getsizeof(docDict)
print "entDict size [bytes]: ", sys.getsizeof(entDict)
print "phraseDict [bytes]: ", sys.getsizeof(phraseDict)



# 2. save the ent and phrase dictionaries
#============================================
#============================================
saveDicts = open(resultEntDictFile, "w")
saveDicts.write(json.dumps(entDict))
saveDicts.close()

saveDicts = open(resultEntDictFile, "w")
for e in entDict.keys():
	saveDicts.write(e+"\n")
saveDicts.close()

saveDicts = open(resultPhraseDictFile, "w")
saveDicts.write(json.dumps(phraseDict))
saveDicts.close() 

saveDicts = open(resultPhraseDictFile, "w")
for p in phraseDict.keys():
	saveDicts.write(p+"\n")
saveDicts.close()

"""
# 3. build tensor 
#============================================
#============================================
T.click()

docDict = dict()

numEnt = len(entDict)
numPhrase = len(phraseDict)
numDoc = len(articles)

tensorFileDir = "/home/aschumilin/"
tensorFile = open(tensorFileDir + "wikinews_tensor.csv", "wb")
fileWriter = csv.writer(tensorFile, delimiter=';', quoting=csv.QUOTE_NONE)

print " building tensor ..."
i = 0
for docName in articles:
	if 1%100 == 0: print ".",
	i += 1

	# build document dictionary: use the article-ID as key 
	docID = docName.split("-")[0]
	if docID not in docDict:
		docDict.update({ docID : docIndex})
		docIndex += 1
	#=========================================


	doc = open(sourceDir + docName, "r")
	
	docSlice = [[False for i in range(numPhrase)] for j in range(numEnt)]
	
	for entityMention in doc:
		# get the cleaned entity and phrase
		returned = extractPhrase(entityMention)
		ent = returned[0].strip()
		phrase = returned[1].strip()
		if ent == "":
			print docName, ": ", entityMention
			continue # avoid broken entity mentions
		if ent[0] == "_":
			ent = ent[1:] 
		if ent[len(ent) - 1] == "_":
			ent = ent[:len(ent) - 1] 
		ent = ent.lower().strip()
		phrase = phrase.replace("\"", "")
		
		
		
		# 1. fetch the index numbers of the entity and phrase from dictionaries
		entIndex = entDict.get(ent)
		phraseIndex = phraseDict.get(phrase)
		
		
		# 2. set 1 in the corresponding field
		docSlice[entIndex][phraseIndex] = True
	
	# append the slice of the current document	
	fileWriter.writerrow(docSlice)

# close result file
tensorFile.close()


# save the doc dictionary to file
saveDicts = open(resultDocDictFile, "w")
saveDicts.write(json.dumps(docDict))
saveDicts.close()






print " allocating tensor memory..."
# build tensor of shape: TENSOR[docIndex][entIndex][phraseIndex]
tensor = [[[0 for i in range(numPhrase)] for j in range(numEnt)] for i in range(numDoc)]

print "done\n building tensor ..."
i = 0
for docName in articles:
	if 1%100 == 0: print ".",
	i += 1


	doc = open(sourceDir + docName, "r")
	
	
	for entityMention in doc:
		# get the cleaned entity and phrase
		returned = extractPhrase(entityMention)
		ent = returned[0].strip()
		phrase = returned[1].strip()
		if ent == "":
			print docName, ": ", entityMention
			continue # avoid broken entity mentions
		if ent[0] == "_":
			ent = ent[1:] 
		if ent[len(ent) - 1] == "_":
			ent = ent[:len(ent) - 1] 
		ent = ent.lower().strip()
		phrase = phrase.replace("\"", "")
		
		
		
		# 1. fetch the index numbers of the entity and phrase from dictionaries
		docIndex = docDict.get(docName.split("-")[0])
		entIndex = entDict.get(ent)
		phraseIndex = phraseDict.get(phrase)
		
		
		
		# 2. set 1 in the corresponding field
		tensor[docIndex][entIndex][phraseIndex] = 1
		
T.click()

print "done \n tensor built in ", T.show()


print " traversing tensor ..."
T.click()

# test:
summe = 0
for d in tensor:
	for e in d:
		for p in e:
			summe += p


T.click()		

print " done \n tensor traversed in ", T.show()

print " summe = entCount?: ", (summe == entCount), " : ", summe
"""
