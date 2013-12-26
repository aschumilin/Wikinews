""" Wikinews explorer GUI """
from Tkinter import Tk, Frame, Scrollbar, Label, Text, Listbox, Button, INSERT, END, ACTIVE, W, E
import tkMessageBox
import os, urllib2, sys
import xml.etree.ElementTree as ET

#from Timer import Timer

def extractEntityName(entityString):
	#allowedPrefs = wikiPrefixes = ['w', 'wikipedia']
	if ":" in entityString:
		if entityString.startswith("w:"):
			rest = entityString.split("w:")[1]
			print "--- ", rest
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
			elif len(parts) ==	4:
				# w|ent|anchor|phrase
				return parts[1].replace(" ", "_")	
				print "detected: (w, wikipedia)|ent|anchor|phrase"

                

class WikinewsExplorer:
	def __init__(self, master):
		
		
		self.currentFileName = ""
		self.entDir = "/dev/shm/wikinews/entities/"
		self.llDir= "/dev/shm/wikinews/lang_links/"
		self.boolFileLoad = False
		self.entFiles = []
		self.llFiles = []
		self.wikinewsBaseURL = "http://en.wikinews.org/?curid="

		frame = Frame(master)
		frame.pack()
		
		frame.columnconfigure(1, weight=1)
		frame.columnconfigure(3, pad=7)
		frame.rowconfigure(3, weight=1)
		frame.rowconfigure(5, pad=7)
		
		self.lbEntFile = Label(frame, text="entities dir: ")
		self.lbEntFile.grid(row=0, column=0)
		
		self.lbLLFile = Label(frame, text="lang links dir: ")
		self.lbLLFile.grid(row=1, column=0)
		
		self.txtEntFile =Text(frame, height=1, width=40)
		self.txtEntFile.insert(INSERT, self.entDir)
		self.txtEntFile.grid(row=0, column=1)
		
		self.txtLLFile =Text(frame, height=1, width=40)
		self.txtLLFile.insert(INSERT, self.llDir)
		self.txtLLFile.grid(row=1, column=1)
		
		self.butLoad= Button(frame, text ="Load", command = self.readInputFiles)
		self.butLoad.grid(row=0, column=2, rowspan=2)
		
		
		
		self.scrollbar = Scrollbar(frame)
		self.lstArticles = Listbox(frame, yscrollcommand = self.scrollbar.set, width=50, height=20)
		self.lstArticles.grid( row=2, column=0, columnspan=2, sticky=W)
		self.lstArticles.bind("<<ListboxSelect>>", self.onArticleSelect)
		
		self.scrollbar.grid(row=2, column=3, sticky=W)
		self.scrollbar.config( command = self.lstArticles.yview )
		
		self.butOpenBrowser = Button(frame, text="Open Article in Firefox", command=self.openInFirefox)
		self.butOpenBrowser.grid(row=3, column=0)
	
	
	
		self.lblSearchTitle = Label(frame, text="search article ID: ")
		self.lblSearchTitle.grid(row=4, column=0, sticky=E)
		
		self.txtSearchTitle = Text(frame, height=1, width=30)
		self.txtSearchTitle.grid(row=4, column=1)
		
		
		self.butSearchTitle = Button(frame, text="Go", command=self.searchTitle)
		self.butSearchTitle.grid(row=4, column=2, sticky=W)
		
		self.scrollbar2 = Scrollbar(frame)		
		self.lstContent = Listbox(frame, yscrollcommand=self.scrollbar2.set, width=100, height=30)
		self.lstContent.grid(row=0, column=3, rowspan=5)
		self.lstContent.bind("<<ListboxSelect>>", self.onEntitySelect)
		self.scrollbar2.grid(row=0, column=3, sticky=W)
		self.scrollbar2.config( command = self.lstContent.yview )
		
		
		self.scrollbar3 = Scrollbar(frame)		
		self.lstWikiLinks = Listbox(frame, yscrollcommand=self.scrollbar3.set, width=70, height=30)
		self.lstWikiLinks.grid(row=5, column=3, sticky=W)
		self.scrollbar3.grid(row=5, column=3, sticky=W)
		self.scrollbar3.config( command = self.lstWikiLinks.yview )
	
	
	
	def onEntitySelect(self, event):
		# enpty content box
		self.lstWikiLinks.delete(0, END)
		widg = event.widget
		index = int(widg.curselection()[0])
		entityString = widg.get(index)
		print 'selected entity %d: "%s"' % (index, entityString)	
		
		entityName = extractEntityName(entityString)
		self.lstWikiLinks.insert(END, "en.wikipedia.org/wiki/" + entityName) 
		self.lstWikiLinks.insert(END, "======= links to the following wiki entities: ========================") 
		
		url = "http://en.wikipedia.org/w/api.php?format=xml&action=query&titles=" + entityName +"&prop=links"
		print "HTTP request: ", url
		xmlResponseTree = None
		try:
			response = urllib2.urlopen(url).read()
			xmlResponseTree = ET.fromstring(response)
		except:
			print " \n ERROR: ", str(sys.exc_info()[0])
								
		
		if xmlResponseTree != None:
			for link in xmlResponseTree.iter("pl"):
# 				item = "en.wikipedia.org/wiki/" + 
				self.lstWikiLinks.insert(END, link.attrib.get("title"))
		else:
			print " xml response tree empty "
		
	def onArticleSelect(self, event):
		
		# enpty content boxes
		self.lstContent.delete(0, END)
		self.lstWikiLinks.delete(0,END)
		
		widg = event.widget
		index = int(widg.curselection()[0])
		fileName = widg.get(index)
		self.currentFileName = fileName
		print 'selected item %d: "%s"' % (index, fileName)	
		
		# load the entity and lang-link files and display in the content box
		entFile = self.entDir + fileName
		llFile = self.llDir + fileName
		ents = open(entFile)
		lls = open(llFile)

		self.lstContent.insert(END, "===== contained Entities =================================")
		
		for ent in ents:
			self.lstContent.insert(END, ent.strip())

		self.lstContent.insert(END, " ")			
		self.lstContent.insert(END, "===== contained Language Links ===========================")
		
		for ll in lls:
			self.lstContent.insert(END, ll.strip())
			
		ents.close()
		lls.close()
		
	def openInFirefox(self):
		wikinewsBase = self.wikinewsBaseURL
		
		articleID = self.lstArticles.get(ACTIVE).split("-")[0]
		
		commandLinux = "firefox " + wikinewsBase + articleID + " &"	
		commandMacOS = "open -a firefox -g " + wikinewsBase + articleID
		commandWindows = 'firefox.exe \"' +  wikinewsBase + articleID +  '\"'
	
	
		if os.uname()[0] == "Linux":
			print "Linux: starting firefox"
			os.system(commandLinux)
		elif os.uname()[0] == "Mac":
			print "Mac: starting firefox"
			os.system(commandMacOS)
		elif os.name == "Windows":
			print "Windows: starting firefox"
			os.system(commandWindows)
		else:
			tkMessageBox.showinfo("Wikinews Explorer", "Strange OS detected: " + os.uname()[0] + "\n can't start Firefox")
		
		return
	
	def searchTitle(self):
		print "search: files loaded?", self.boolFileLoad
		targetString = self.txtSearchTitle.get(1.0, END).strip()
		if self.boolFileLoad:
			i = 0
			for fileName in self.entFiles:
				if targetString.lower() in fileName.lower():
					# focus first result and exit
					
					self.lstArticles.selection_set(i, i)
					self.lstArticles.see(i)
				
					
					print "--- found: ", i, " ", fileName
					break
				i += 1
				
		else:
			tkMessageBox.showinfo("Wikinews Explorer", "Input files not loaded")
	
	
	def readInputFiles(self):
		self.entDir = self.txtEntFile.get(1.0, END).strip()
		self.llDir = self.txtLLFile.get(1.0, END).strip()

		if not os.path.exists(self.entDir):
			tkMessageBox.showinfo( "Wikinews Explorer", self.entDir + "\ndoes not exist")
			self.boolFileLoad = False
			return
		if not os.path.exists(self.llDir):
			self.boolFileLoad = False
			tkMessageBox.showinfo( "Wikinews Explorer", self.llDir + "\ndoes not exist")
			return	
		
		# no return until here, it's fine
		self.entFiles = os.listdir(self.entDir)
		self.llFiles = os.listdir(self.llDir)
		
		if len(self.entFiles) != len(self.llFiles):
			tkMessageBox.showinfo("Wikinews Explorer", "something's wrong: \n  article number mismatch: " + len(self.entFiles) + " != " + len(self.llFiles))
			self.boolFileLoad = False
			return
		else:
			print "files count ok: ", str(len(self.entFiles)), " == ", str(len(self.llFiles))
			for fileName in self.entFiles:
				self.lstArticles.insert(END, fileName)
			self.boolFileLoad = True # file loading ok
		
		print "files loaded?", self.boolFileLoad


root = Tk()
root.title("Wikinews Explorer")
#root.geometry("200x85")
app = WikinewsExplorer(root)
root.mainloop()


















