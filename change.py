import json


paths = ["/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/wikinews_2013-10-30_sparse_tensor_repr/doc_dict.json", "/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/wikinews_2013-10-30_sparse_tensor_repr/ent_dict.json", "/home/aifb/stud/ls3/atsc/en_wikinews_2013-10-30/wikinews_2013-10-30_sparse_tensor_repr/phrase_dict.json"]


for path in paths:
	dic = json.load(open(path, "r"))
	changed = dict()
	
	for item in dic:
		changed.update({dic.get(item) : item})
		
	if not (len(dic) == len(changed)):
		print "ERROR: dict length mismatch: ", str(len(dic)) , " != ", str(len(changed))
		print "in ", path
	print "done: ", path	
	f = open (path, "w")
	f.write(json.dumps(changed))
	f.close()
	print "saved: ", path
		
		

