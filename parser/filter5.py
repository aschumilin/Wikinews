""" remove articles containing less than (<) X entity mentions
/media/MYLINUXLIVE/AIFB/Wikinews/parser/filter5.py"""
# 741194 [[...]] elements in dump 
# 205647 non-namespace candidates
# 190383 non-namespace and non-'Image'
# 188452 non-namespace and non-'Image' and non-'category'


import os, codecs 
from shutil import copyfile
from Timer import Timer

T = Timer()


sourceDirEnts = "/dev/shm/wikinews/entities/"
sourceDirLanglinks = "/dev/shm/wikinews/lang_links/"

resultDirEnts = "/dev/shm/wikinews/entities_pruned/"
resultDirLanglinks = "/dev/shm/wikinews/lang_links_pruned/"

if not os.path.exists(resultDirEnts):
	os.makedirs(resultDirEnts)
if not os.path.exists(resultDirLanglinks):
    os.makedirs(resultDirLanglinks)
    

articles = os.listdir(sourceDirEnts)

T.click()

###################
###################
###################
minNumMentions = 3
###################
###################
###################

numThinArticles = 0

for fileName in articles:
	
	article = open(sourceDirEnts + fileName, "r")
	numEntityMentions = 0
	for entity in article:
		# count entities in each article
		numEntityMentions += 1

	article.close()
	if numEntityMentions < minNumMentions:
		# this article contains too few entity mentions
		numThinArticles += 1
	else: 	
		# copy good article (corresponding entities and lang_links file) to target dir
		# shutil.copyfile("sourcefile", "destfile")
		copyfile(sourceDirEnts + fileName, resultDirEnts + fileName)
		copyfile(sourceDirLanglinks + fileName, resultDirLanglinks + fileName)
		
	



T.click()

print "numThinArticles: ", numThinArticles
print "done in ", T.show()
    
    
    
# minNumMentions = 3:
# numThinArticles:  3735
# number of good articles: 15725 (containing 161744 entity mentions)
    


# minNumMentions = 5:
# numThinArticles:  7205
# number of good articles: 12255
    
    
    
   #rm -rf /dev/shm/wikinews/entities_pruned/ /dev/shm/wikinews/lang_links_pruned/

    
    
    
    
    
    
    
    
    
    
    
    
