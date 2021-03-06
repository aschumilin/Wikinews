""" gettting the entities for each document 
/media/MYLINUXLIVE/AIFB/Wikinews/parser/filter3.py"""
# 741194 [[...]] elements in dump 
# 205647 non-namespace candidates
# 190383 non-namespace and non-'Image'
# 188452 non-namespace and non-'Image' and non-'category'

import xml.etree.ElementTree as ET
import os, re, codecs 
from Timer import Timer

T = Timer()

# all prefixes to lower case !!!!!!!!!!!!!!
forbiddenPrefixes = ['media', 'special', 'talk', 'user', 'user talk', 'wikinews', 'wikinews talk', 'file', 'file talk', 'mediawiki', 'mediawiki talk', 'template', 'template talk', 'help', 'help talk', 'category', 'category talk', 'thread', 'thread talk', 'summary', 'summary talk', 'portal', 'portal talk', 'comments', 'comments talk', 'education program', 'education program talk', 'module', 'module talk', 'image', 'talk', 'file', 'news briefs', 'category', 'cat', 'commons', 'wiktionary', 'wikt', 'wikisource', 'wikifur', 'wn', 'meta', 'foundation', 'm', 'meta', 'mw', 'foundation',  'wikt',  's', 'b', 'wiki'] 
langPrefixes = ['en', 'de', 'fr', 'nl', 'it', 'es', 'ru', 'sv', 'pl', 'ja', 'pt', 'ar', 'zh', 'uk', 'ca', 'no', 'fi', 'cs', 'hu', 'tr', 'ro', 'sw', 'ko', 'kk', 'vi', 'da', 'eo', 'sr', 'id', 'lt', 'vo', 'sk', 'he', 'fa', 'bg', 'sl', 'eu', 'war', 'lmo', 'et', 'hr', 'new', 'te', 'nn', 'th', 'gl', 'el', 'ceb', 'simple', 'ms', 'ht', 'bs', 'bpy', 'lb', 'ka', 'is', 'sq', 'la', 'br', 'hi', 'az', 'bn', 'mk', 'mr', 'sh', 'tl', 'cy', 'io', 'pms', 'lv', 'ta', 'su', 'oc', 'jv', 'nap', 'nds', 'scn', 'be', 'ast', 'ku', 'wa', 'af', 'be-x-old', 'an', 'ksh', 'szl', 'fy', 'frr', 'yue', 'ur', 'ia', 'ga', 'yi', 'als', 'hy', 'am', 'roa-rup', 'map-bms', 'bh', 'co', 'cv', 'dv', 'nds-nl', 'fo', 'fur', 'glk', 'gu', 'ilo', 'kn', 'pam', 'csb', 'km', 'lij', 'li', 'ml', 'gv', 'mi', 'mt', 'nah', 'ne', 'nrm', 'se', 'nov', 'qu', 'os', 'pi', 'pag', 'ps', 'pdc', 'rm', 'bat-smg', 'sa', 'gd', 'sco', 'sc', 'si', 'tg', 'roa-tara', 'tt', 'to', 'tk', 'hsb', 'uz', 'vec', 'fiu-vro', 'wuu', 'vls', 'yo', 'diq', 'zh-min-nan', 'zh-classical', 'frp', 'lad', 'bar', 'bcl', 'kw', 'mn', 'haw', 'ang', 'ln', 'ie', 'wo', 'tpi', 'ty', 'crh', 'jbo', 'ay', 'zea', 'eml', 'ky', 'ig', 'or', 'mg', 'cbk-zam', 'kg', 'arc', 'rmy', 'gn', 'so', 'kab', 'ks', 'stq', 'ce', 'udm', 'mzn', 'pap', 'cu', 'sah', 'tet', 'sd', 'lo', 'ba', 'pnb', 'iu', 'na', 'got', 'bo', 'dsb', 'chr', 'cdo', 'hak', 'om', 'my', 'sm', 'ee', 'pcd', 'ug', 'as', 'ti', 'av', 'bm', 'zu', 'pnt', 'nv', 'cr', 'pih', 'ss', 've', 'bi', 'rw', 'ch', 'arz', 'xh', 'kl', 'ik', 'bug', 'dz', 'ts', 'tn', 'kv', 'tum', 'xal', 'st', 'tw', 'bxr', 'ak', 'ab', 'ny', 'fj', 'lbe', 'ki', 'za', 'ff', 'lg', 'sn', 'ha', 'sg', 'ii', 'cho', 'rn', 'mh', 'chy', 'ng', 'kj', 'ho', 'mus', 'kr', 'hz', 'mwl', 'pa', 'xmf', 'lez', 'chm']

wikiPrefixes = ['w', 'wikipedia']
allowedPrefixes = wikiPrefixes # + langPrefixes 

defaultNamespace = "{http://www.mediawiki.org/xml/export-0.8/}"


sourceDir = "/dev/shm/wikinews/articles_cleaned/"
resultDir = "/dev/shm/wikinews/candidates_good/"
resultBadDir = "/dev/shm/wikinews/candidates_bad/"
if not os.path.exists(resultDir):
    os.makedirs(resultDir)
if not os.path.exists(resultBadDir):
    os.makedirs(resultBadDir)


articles = os.listdir(sourceDir) 

cands = [] # candidate entities
T.click()
numberEntityCands = 0

strangePrefixes = codecs.open("/dev/shm/wikinews/strangePrefixes", "w", "utf-8")
goodPrefixes = codecs.open("/dev/shm/wikinews/goodPrefixes", "w", "utf-8")

j = 0
i = 0
t = 0
for fileName in articles:
    
    # 1. extract article text
    root = ET.parse(sourceDir + fileName).getroot()
    artText = root.find(".//" + defaultNamespace + "text").text

    # 2. find all candidate entities:
    # consider [[...]] and {{w|...}} patterns
    cands = re.findall("\[\[(.+?)\]\]", artText)
    cands2 = re.findall("\{\{(.+?)\}\}", artText)

    # 3. open result file (same name as article file) to write candidate entities per article
    resultFile = codecs.open(resultDir + fileName, "w", "utf-8")
    resultBadFile = codecs.open(resultBadDir + fileName, "w", "utf-8")
    

    # [[...]]
    
    for cand in cands:

        prefix1 = cand.split(":")[0].lower() # !!!!!!!!!!! lower case !!!!!!!!!!!!!!!!!!!!!!
        length = len(cand.split(":"))


        # ...:user: ... is not an good entity
        if ":user:" in cand.lower():
            j += 1
            continue
        if "category:wikipedia" in cand.lower():
            j += 1
            continue         
        if cand.lower().startswith("w:|"):
            print cand, "\n"
            # this is a broken link
            j += 1
            t +=1
            continue
        if length > 2 and (cand.split(":")[1].lower() in langPrefixes): 
            # this is a link to wikipedia entity in a specific language
            j +=1
            continue
        
        """
        23419-Energy_companies_to_raise_consumer_rates :  w:

192625-New_'failed_states_index'_report_published :  Wikipedia:|Wikipedia

73519-Anwar's_lawsuit_over_gay_slur_by_former_Mala :  Wikipedia||Mahathir bin Mohamad

193250-Russian_police_to_'check'_officer_allegedly :  Wikipedia:|Wikipedia
        """        

        
        if prefix1 in allowedPrefixes and (length > 1):
            numberEntityCands += 1
            resultFile.write(cand + "\n")
            goodPrefixes.write("[[" + cand + "\n")
        else:
            prefix2 = ""
            try:
                prefix2 = cand.split(":")[1].lower() # !!!!!!!!!!! lower case !!!!!!!!!!!!!!!!!!!!!!
                if prefix2 in allowedPrefixes:
                    numberEntityCands += 1
                    resultFile.write(cand + "\n")
                    goodPrefixes.write("[[" + cand + "\n")
                else:
                    resultBadFile.write(cand + "\n")                    
                    strangePrefixes.write("[[" + cand[0:50] + "\n")
            except:
                i += 1
        if (i % 100) == 0:
            print ".", #"prefix2 Error   ", cand    



    # {{...}}
    for cand in cands2:
        prefix1 = cand.split("|")[0].lower() # !!!!!!!!!!! lower case !!!!!!!!!!!!!!!!!!!!!!
        length = len(cand.split("|"))
        
            
            
        
        if prefix1 in allowedPrefixes and (length > 1):
            if length > 1:            
                numberEntityCands += 1
                resultFile.write(cand + "\n")
                goodPrefixes.write("{{" + cand + "\n")
        else:
            resultBadFile.write(cand + "\n")                    
            strangePrefixes.write("{{" + cand[0:50] + "\n")

    
    resultFile.close()
    resultBadFile.close()    

strangePrefixes.close()
goodPrefixes.close()
T.click()
print " j ", j
print str(numberEntityCands) , " ent cands in " , T.show()
print "w:| ??", t
"""
def classifyCnadidateEntity(entityString):
    # classifier for [[...]] and {{...}} candidates 
        
    allowedPrefs = wikiPrefixes = ['w', 'wikipedia']
    langPrefixes = ['en', 'de', 'fr', 'nl', 'it', 'es', 'ru', 'sv', 'pl', 'ja', 'pt', 'ar', 'zh', 'uk', 'ca', 'no', 'fi', 'cs', 'hu', 'tr', 'ro', 'sw', 'ko', 'kk', 'vi', 'da', 'eo', 'sr', 'id', 'lt', 'vo', 'sk', 'he', 'fa', 'bg', 'sl', 'eu', 'war', 'lmo', 'et', 'hr', 'new', 'te', 'nn', 'th', 'gl', 'el', 'ceb', 'simple', 'ms', 'ht', 'bs', 'bpy', 'lb', 'ka', 'is', 'sq', 'la', 'br', 'hi', 'az', 'bn', 'mk', 'mr', 'sh', 'tl', 'cy', 'io', 'pms', 'lv', 'ta', 'su', 'oc', 'jv', 'nap', 'nds', 'scn', 'be', 'ast', 'ku', 'wa', 'af', 'be-x-old', 'an', 'ksh', 'szl', 'fy', 'frr', 'yue', 'ur', 'ia', 'ga', 'yi', 'als', 'hy', 'am', 'roa-rup', 'map-bms', 'bh', 'co', 'cv', 'dv', 'nds-nl', 'fo', 'fur', 'glk', 'gu', 'ilo', 'kn', 'pam', 'csb', 'km', 'lij', 'li', 'ml', 'gv', 'mi', 'mt', 'nah', 'ne', 'nrm', 'se', 'nov', 'qu', 'os', 'pi', 'pag', 'ps', 'pdc', 'rm', 'bat-smg', 'sa', 'gd', 'sco', 'sc', 'si', 'tg', 'roa-tara', 'tt', 'to', 'tk', 'hsb', 'uz', 'vec', 'fiu-vro', 'wuu', 'vls', 'yo', 'diq', 'zh-min-nan', 'zh-classical', 'frp', 'lad', 'bar', 'bcl', 'kw', 'mn', 'haw', 'ang', 'ln', 'ie', 'wo', 'tpi', 'ty', 'crh', 'jbo', 'ay', 'zea', 'eml', 'ky', 'ig', 'or', 'mg', 'cbk-zam', 'kg', 'arc', 'rmy', 'gn', 'so', 'kab', 'ks', 'stq', 'ce', 'udm', 'mzn', 'pap', 'cu', 'sah', 'tet', 'sd', 'lo', 'ba', 'pnb', 'iu', 'na', 'got', 'bo', 'dsb', 'chr', 'cdo', 'hak', 'om', 'my', 'sm', 'ee', 'pcd', 'ug', 'as', 'ti', 'av', 'bm', 'zu', 'pnt', 'nv', 'cr', 'pih', 'ss', 've', 'bi', 'rw', 'ch', 'arz', 'xh', 'kl', 'ik', 'bug', 'dz', 'ts', 'tn', 'kv', 'tum', 'xal', 'st', 'tw', 'bxr', 'ak', 'ab', 'ny', 'fj', 'lbe', 'ki', 'za', 'ff', 'lg', 'sn', 'ha', 'sg', 'ii', 'cho', 'rn', 'mh', 'chy', 'ng', 'kj', 'ho', 'mus', 'kr', 'hz', 'mwl', 'pa', 'xmf', 'lez', 'chm']


    #if ":" in entityString:
    if entityString.startswith("w:"):
        rest = entityString.split("w:")[1]
        if "|" in rest: return extractEntityName("w|" + rest)
    elif entityString.startswith(":w:"):
        rest = entityString.split(":w:")[1]
        if "|" in rest: return extractEntityName("w|" + rest)
    elif entityString.startswith("wikipedia:"):
        rest = entityString.split("wikipedia:")[1]
        if "|" in rest: return extractEntityName("w|" + rest)
    elif entityString.startswith(":wikipedia:"):
        rest = entityString.split(":wikipedia:")[1]
        if "|" in rest: return extractEntityName("w|" + rest)
    
    if "|" in entityString:
        parts = entityString.split("|")
        
        if (parts[0].lower() == "w") or (parts[0].lower() == "wikipedia"):
            if len(parts) == 2:
                # w|ent
                return parts[1].replace(" ", "_")     
                print "detected: (w, wikipedia)|ent"
            elif len(parts) == 3:
                # w|ent|phrase
                return parts[1].replace(" ", "_")
                print "detected: (w, wikipedia)|ent|phrase"
            elif len(parts) ==    4:
                # w|ent|anchor|phrase
                return parts[1].replace(" ", "_")    
                print "detected: (w, wikipedia)|ent|anchor|phrase"

 
def extractEntityName(entityString):
    #allowedPrefs = wikiPrefixes = ['w', 'wikipedia']
    #if ":" in entityString:
    if entityString.lower().startswith("w:"):
        rest = entityString.split("w:")[1]
        #print "--- ", rest
        if "|" in rest: return extractEntityName("w|" + rest)
    elif entityString.startswith(":w:"):
        rest = entityString.split(":w:")[1]
        if "|" in rest: return extractEntityName("w|" + rest)
    elif entityString.startswith("wikipedia:"):
        rest = entityString.split("wikipedia:")[1]
        if "|" in rest: return extractEntityName("w|" + rest)
    elif entityString.startswith(":wikipedia:"):
        rest = entityString.split(":wikipedia:")[1]
        if "|" in rest: return extractEntityName("w|" + rest)
    
    if "|" in entityString:
        parts = entityString.split("|")
        
        if (parts[0].lower() == "w") or (parts[0].lower() == "wikipedia"):
            if len(parts) == 2:
                # w|ent
                return parts[1].replace(" ", "_")     
                print "detected: (w, wikipedia)|ent"
            elif len(parts) == 3:
                # w|ent|phrase
                return parts[1].replace(" ", "_")
                print "detected: (w, wikipedia)|ent|phrase"
            elif len(parts) ==    4:
                # w|ent|anchor|phrase
                return parts[1].replace(" ", "_")    
                print "detected: (w, wikipedia)|ent|anchor|phrase"

     
    
"""
    
"""
pilatus@comp:/dev/shm/wikinews/entities$ grep ":w:" ./*| wc -l
3018
pilatus@comp:/dev/shm/wikinews/entities$ grep "w|" ./*| wc -l
31650
pilatus@comp:/dev/shm/wikinews/entities$ grep "wikipedia|" ./*| wc -l
434
pilatus@comp:/dev/shm/wikinews/entities$ grep "wikipedia:" ./*| wc -l
192
pilatus@comp:/dev/shm/wikinews/entities$ grep ":wikipedia:" ./*| wc -l
17
pilatus@comp:/dev/shm/wikinews/entities$ grep "w:" ./*| wc -l
132284
"""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
