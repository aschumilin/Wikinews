""" 
extract the pure entity names and separate the phrases. Do additional cleaning:
e.g. entity: _Angela_Merkel = _Angela_Merkel_ = Angela_Merkel = angela_merkel
e.g. phrase: "Forbes Magazine" = "Forbes" magazine
"""

# tensor factorization: github mnick - Maximilian Nickel
# mData = loadmat("/path/file.mat")

from scipy.io.matlab import loadmat
import os
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
            elif len(parts) ==    4:
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

articles = os.listdir(sourceDir)

entCount = 0
entDict = dict()
phraseDict = dict()
entIndex = 0
phraseIndex = 0
j = 0
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
            if entity.lower().startswith("w:|"):
            	print entity
            	print "-", ent, "-"
            	j += 1
            #########
            #########
            # clean entities and 
            # 1. cut off a leading undescore
            """ent = ent.strip()
            if ent == "":
            	print fileName, ": ", entity
            if ent[0] == "_":
                ent = ent[1:] 
                
            # 2. cut off trailing underscore
            if ent[len(ent)-1] == "_":
                ent = ent[:len(ent)-1] 
                
            # 3. transfer to lower case and strip blanks
            ent = ent.lower().strip()
            
            # 4. remove all " from phrases
            phrase = phrase.replace("\"", "")
            
            """
            
            
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
                
                
                

        else:
            print "===============", fileName, "======="
            print "    bad Entity mention: ", entity


resultFile.close()

T.click()
print "-", j, "-"

print "=== SUMMARY ==="
print "dictionaries building done in ", T.show()
print "found ", entCount, " entity mentions in ", len(articles), " articles"
print " number of distinct entities: ", len(entDict)
print " referred to by ", len(phraseDict), " distinct phrases"

"""
=== SUMMARY (before cleaning ===
dictionaries building done in  1.06981611252s
found  161744  entity mentions in  15723  articles
 number of distinct entities:  67323
 referred to by  69890  distinct phrases
"""



# 2. build tensor 
#============================================
#============================================
tf = open("/dev/shm/wikinews/DE.txt", "w")
for e in entDict:
	tf.write(e + "\n")
tf.close()
tf = open("/dev/shm/wikinews/DP.txt", "w")
for p in phraseDict:
	tf.write(p+"\n")
tf.close()
	





