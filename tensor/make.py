# github mnick - Maximilian Nickel
# mData = loadmat("/path/file.mat")

from scipy.io.matlab import loadmat



def extractEntityName(entityString):
    #allowedPrefs = wikiPrefixes = ['w', 'wikipedia']
    if ":" in entityString:
        if entityString.startswith("w:"):
            rest = entityString.split("w:")[1]
            
            if "|" in rest: return extractEntityName("w|" + rest)
            else: return extractEntityName("w|" + rest)
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
                
   
   
s = "w:es:asdasd|sdfsdf"   
r = extractEntityName(s)     
if (r == None): print "empty return"   
print '%s ~ %s' % (r[0], r[1])    



