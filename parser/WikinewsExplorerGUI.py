""" Wikinews explorer GUI """
from Tkinter import *
import tkMessageBox
import os


entDir = ""
llDir = ""
boolFileLoad = False
print "init done"
entFiles = []
llFiles = []
root = Tk()
root.title("Wikinews Explorer")


def openInFirefox():
	wikinewsBaseURL = "http://en.wikinews.org/?curid="
	
	 
	articleID = lstArticles.get(ACTIVE).split("-")[0]
	
	commandLinux = "firefox " + wikinewsBaseURL + articleID	
	commandMacOS = "open -a firefox -g " + wikinewsBaseURL + articleID
	commandWindows = 'firefox.exe \"' +  wikinewsBaseURL + articleID +  '\"'

	print commandMacOS

	if os.uname()[0] == "Linux":
		print "Linux: starting firefox"
		os.system(commandLinux)
	elif os.uname()[0] == "Mac":
		print "Mac: starting firefox"
		os.system(commandMac)
	elif os.name == "Windows":
		print "Windows: starting firefox"
		os.system(commandWindows)
	else:
		tkMessageBox.showinfo("Wikinews Explorer", "Strange OS detected: " + os.uname()[0] + "\n can't start Firefox")
	
	return

def searchTitle():
	print "search: files loaded?", boolFileLoad
	targetString = txtSearchTitle.get(1.0, END).strip()
	if not boolFileLoad:
		i = 0
		for fileName in entFiles:
			i += 1
			print fileName
			if fileName.lower().contains(targetString.lower()):
				# focus first result and exit
				lstArticles.selection_anchor(i)
				print "--- found:", i
				break
			
	else:
		tkMessageBox.showinfo("Wikinews Explorer", "Input files not loaded")


def readInputFiles():
	entDir = txtEntFile.get(1.0, END).strip()
	llDir = txtLLFile.get(1.0, END).strip()
	#s = "-load "+entDir+"\n-load "+llDir
	#print s
	if not os.path.exists(entDir):
		tkMessageBox.showinfo( "Wikinews Explorer", entDir + "\ndoes not exist")
		boolFileLoad = False
		return
	if not os.path.exists(llDir):
		boolFileLoad = False
		tkMessageBox.showinfo( "Wikinews Explorer", llDir + "\ndoes not exist")
		return	
	
	# no return until here, it's fine
	entFiles = os.listdir(entDir)
	llFiles = os.listdir(llDir)
	
	if len(entFiles) != len(llFiles):
		tkMessageBox.showinfo("Wikinews Explorer", "something's wrong: \n  article number mismatch: " + len(entFiles) + " != " + len(llFiles))
		boolFileLoad = False
		return
	else:
		print "files count ok: ", str(len(entFiles)), " == ", str(len(llFiles))
		for fileName in entFiles:
			lstArticles.insert(END, fileName)
		boolFileLoad = True # file loading ok
	
	print "files loaded?", boolFileLoad





lbEntFile = Label(root, text="entities dir: ")
lbEntFile.grid(row=0, column=0)

lbLLFile = Label(root, text="lang links dir: ")
lbLLFile.grid(row=1, column=0)

txtEntFile =Text(root, height=1)
txtEntFile.insert(INSERT, "/dev/shm/wikinews/entities/")
txtEntFile.grid(row=0, column=1)

txtLLFile =Text(root, height=1)
txtLLFile.insert(INSERT, "/dev/shm/wikinews/lang_links/")
txtLLFile.grid(row=1, column=1)

butLoad= Button(root, text ="Load", command = readInputFiles)
butLoad.grid(row=0, column=2, rowspan=2)



scrollbar = Scrollbar(root)
lstArticles = Listbox(root, yscrollcommand = scrollbar.set, width=50, height=20)
lstArticles.grid( row=2, column=0, columnspan=2, sticky=W)
scrollbar.grid(row=2, column=3, sticky=W)
scrollbar.config( command = lstArticles.yview )

butOpenBrowser = Button(root, text="Open in Firefox", command=openInFirefox)
butOpenBrowser.grid(row=2, column=1, sticky=E)



lblSearchTitle = Label(root, text="search titles: ")
lblSearchTitle.grid(row=4, column=0)

txtSearchTitle = Text(root, height=1)
txtSearchTitle.grid(row=4, column=1)


butSearchTitle = Button(root, text="Go", command=searchTitle)
butSearchTitle.grid(row=4, column=2)

"""
def searchEntity():
	if boolFileLoad == True:
		# display search results
	else:
		tkMessageBox.showinfo("Wikinews Explorer", "Input files not loaded")
lblSearchID = Label(root, text="search entities: ")
lblSearchID.grid(row=5, column=0)

txtSearchEntity = Text(root, height=1)
txtSearchEntity.grid(row=5, column=1)

butSearchEntity = Button(root, text="Go", command=searchEntity)
butSearchEntity.grid(row=5, column=2)
"""



"""
text = Text(root)
text.insert(INSERT, "Hello.....")
text.grid(row=3, column=0, columnspan=2)
"""






root.mainloop()




