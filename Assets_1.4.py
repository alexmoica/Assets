#Assets 2018 © Alex Moica

import tkinter as tk
from tkinter import simpledialog
import os
import re
import sys
import time
import matplotlib
matplotlib.use('TkAgg') #set matplotlib to use tkinter anti-grain geometry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#define custom typesets
LARGE_FONT = ('Verdana 10 underline')
BOLD_FONT = ('Verdana 9 bold')

#define paths to current directory
dp = os.path.join(os.path.dirname(__file__),'Logs\\')
imgp = os.path.join(os.path.dirname(__file__),'AssetsIcon.ico')

#if Logs directory does not exist, create it
if not os.path.exists(dp):
    os.makedirs(dp)

#function to open a file in given mode, and create the file if it does not exist
def fileOpen(path, type):
	if os.path.exists(path):
		fileName = open(path, type)
		return fileName
	else:
		fileName = open(path, 'w')
		return fileName

#special case for balFile since it needs to write default entries if it does not exist
if os.path.exists(dp+'balance.txt'):
	balFile = open(dp+'balance.txt', 'r')
else:
	balFile = open(dp+'balance.txt', 'w')
	balFile.write("0.0\n0.0\n0.0")
	balFile.close()
	balFile = open(dp+'balance.txt', 'r')

baseVals = balFile.readlines()

recFile = fileOpen(dp+'records.txt', 'r')
optionFile = fileOpen(dp+'note options.txt', 'r')

nOptions = [] #the list of all possible options a note can have - used for AutoComplete class
try:
	for line in optionFile.readlines():
		nOptions.append(line)
except:
	os.execl(sys.executable, sys.executable, *sys.argv) #if the list is empty then internally restart the program, user will not notice
	
balFile.close()
recFile.close()
optionFile.close()

cBalance = float("%.2f" % float(baseVals[0]))
ccBalance = float("%.2f" % float(baseVals[1]))
sBalance = float("%.2f" % float(baseVals[2]))
ccLimit = 1000.00

if ccBalance > 0.0:
	balCol = 'red'
else:
	balCol = 'green'

#change the Tk window to display only the given frame
def showFrame(page):
		page.grid(row=0, column=0, sticky='nsew')
		page.tkraise()

#provide options for user of previously written notes while writing a note
class AutoComplete(tk.Entry):
	def __init__(self, entries, *args, **kwargs):
		tk.Entry.__init__(self, *args, **kwargs)
		self.entries = entries
		self.var = self['textvariable']
		
		#define text input variable
		if self.var == '':
			self.var = self['textvariable'] = tk.StringVar()
		
		self.var.set("(Note)")
		self.var.trace('w', self.update) #update on write
		self.bind('<Return>', self.select)
		self.bind('<Up>', self.up)
		self.bind('<Down>', self.down)
		
		self.lb_up = False
		self.lb = tk.Listbox()
	
	#define button functions, remove listbox if entry is empty
	def update(self, name, index, mode):
		if self.var.get() == '':
			self.lb_up = False
			self.lb.destroy()
		else:
			words = self.compare()
			if words:
				if not self.lb_up:
					self.lb = tk.Listbox()
					self.lb.bind('<Double-Button-1>', self.select)
					self.lb.bind('<Return>', self.select)
					self.lb.bind('<Leave>', self.notFocused)
					self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
					self.lb_up = True
				
				self.lb.delete(0, 'end')
				for i in words:
					self.lb.insert('end', i)
			else:
				if self.lb_up:
					self.lb.destroy()
					self.lb_up = False
	
	#delete listbox if mouse leaves it
	def notFocused(self, event):
		if self.lb_up:
			self.lb.destroy()
			self.lb_up = False
			self.icursor('end')
	
	def select(self, event):
		if self.lb_up:
			self.var.set(self.lb.get('active'))
			self.lb.destroy()
			self.lb_up = False
			self.icursor('end')
			
	def up(self, event):
		if self.lb_up:
			#if no entry is selected and up is called, index is last entry
			if self.lb.curselection() == () or self.lb.curselection() == (0,):
				index = str(self.lb.size()-1)
			else:
				index = str(int(self.lb.curselection()[0])-1) #otherwise index is entry above the selected entry
				
			#when index is not last, activate the entry at the index and inactivate the entry below it
			if index != str(self.lb.size()-1):
				self.lb.selection_clear(first=str(int(index)+1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)-1)
			#if the index is the last one, inactivate the first entry and activate the last entry
			else:
				self.lb.selection_clear(first='0')
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)-1)
				
	def down(self, event):
		if self.lb_up:
			#if no entry is selected or the last entry is selected and down is called, index is first entry
			if self.lb.curselection() == () or self.lb.curselection() == (self.lb.size()-1,):
				index = '0'
			else:
				index = str(int(self.lb.curselection()[0])+1) #otherwise index is entry below the selected entry 
			
			#when index is the first entry, inactivate the last entry and activate the first entry
			if index == '0':
				self.lb.selection_clear(first=str(self.lb.size()-1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)+1)
			#otherwise inactivate previous entry and activate index entry
			else:
				self.lb.selection_clear(first=str(int(index)-1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)+1)
	
	#compare written characters to previous options
	def compare(self):
		pattern = re.compile('.*' + self.var.get().upper() + '.*') #compile re to re object allowing for match to be used on its elements
		return [i for i in self.entries if re.match(pattern, i)] #takes each character in the string entry and compares it to each character in each note option
	
class HomePage(tk.Frame):	
	def __init__(self, master):			
		tk.Frame.__init__(self, master)
		
		root.geometry('306x155')
		root.resizable(width=False, height=True)
		
		tk.Label(self, text=" "*100).grid(row=0, column=0, columnspan=50) #create spacer label for total columns in the frame
		
		accLbl = tk.Label(self, text="Accounts", font=LARGE_FONT).grid(row=0, column=0, columnspan=12, sticky='ew')
		
		def changeCredit():
			global ccLimit
			ccLimit = simpledialog.askinteger("Change Credit Limit", "Please enter a new limit:", minvalue = 0)
			
		ccLimBtn = tk.Button(self, text="Change Credit Limit", width=15, relief='groove', command=changeCredit)
		ccLimBtn.grid(row=0, column=1, columnspan=50, sticky='e')
		
		#chequing Objects
		cLbl = tk.Label(self, text="Chequing").grid(row=1, column=0, columnspan=10, sticky='w')
		cdLbl = tk.Label(self, text=". "*29).grid(row=1, column=1, columnspan=38, sticky='e')
		cBtn = tk.Button(self, text="$"+str(cBalance), fg='green', activeforeground='green', width=10, command=lambda: showFrame(Page(root, "Chequing", 'C', cBalance))) #lambda links tkinter to callback expression
		cBtn.grid(row=1, column=2, columnspan=50, sticky='e')
		
		#credit Objects
		ccLbl = tk.Label(self, text="Credit").grid(row=2, column=0, columnspan=10, sticky='w')
		ccdLbl = tk.Label(self, text=". "*32).grid(row=2, column=1, columnspan=38, sticky='e')
		ccBtn = tk.Button(self, text="$"+str(ccBalance), fg=balCol, activeforeground=balCol, width=10, command=lambda: showFrame(Page(root, "Credit", 'CC', ccBalance)))
		ccBtn.grid(row=2, column=2, columnspan=50, sticky='e')
		
		#savings Objects
		sLbl = tk.Label(self, text="Savings").grid(row=3, column=0, columnspan=10, sticky='w')
		sdLbl = tk.Label(self, text=". "*31).grid(row=3, column=1, columnspan=38, sticky='e')
		sBtn = tk.Button(self, text="$"+str(sBalance), fg='green', activeforeground='green', width=10, command=lambda: showFrame(Page(root, "Savings", 'S', sBalance)))
		sBtn.grid(row=3, column=2, columnspan=50, sticky='e')
		
		#delete text on call
		def amountDelete(event):
			entry_widget.delete(0, 'end')
		
		#delete note text on call
		def noteDelete(event):
			if note_entry.get() != '':
				note_entry.lb_up = True
			else:
				note_entry.lb_up = False
				
			note_entry.delete(0, 'end')
		
		#input objects
		eDollar = tk.Label(self, text="$", font=BOLD_FONT).grid(row=4, column=1, columnspan=36, sticky='e')
		entry_text = tk.StringVar()
		entry_text.set("0.00")
		
		entry_widget= tk.Entry(self, relief='flat', width=5, textvariable=entry_text)
		entry_widget.grid(row=4, column=2, columnspan=40, sticky='e')
		entry_widget.bind('<Button-1>', amountDelete)

		errorLabel = tk.Label(self, text="", font=BOLD_FONT, fg='red')
		errorLabel.grid(row=5, column=0, columnspan=70, sticky='w')
			
		#add new records and balances to their respective files
		def addToFile(acc, val, note):
			global cBalance, ccBalance, sBalance, nOptions
			
			balF = open(dp+'balance.txt', 'w')
			balF.write(str(cBalance)+"\n"+str(ccBalance)+"\n"+str(sBalance)+"\n")
			balF.close()
			
			recF = open(dp+'records.txt', 'a')
			recF.write(acc+", "+str("%.2f" % val)+", "+note.upper().strip()+", "+time.strftime("%Y-%m-%d")+"\n")
			recF.close()
			
			opF = open(dp+'note options.txt', 'r')
			nOptions = opF.readlines()
			opF.close()
			
			opF = open(dp+'note options.txt', 'a')
			if note.upper().strip()+"\n" not in nOptions:
				opF.write(note.upper()+"\n")
				note_entry.entries.append(note.upper())
			opF.close()
		
		def PlusClick():
			global cBalance, ccBalance, sBalance, ccLimit
			isFloat = True
			if accVar.get() == "(Account)":
				errorLabel['text'] = "Please Choose an Account"
			elif note_entry.get() == "(Note)" or note_entry.get().isspace() or not note_entry.get():
				errorLabel['text'] = "Please Choose or Write a Note"
			else:
				try:
					float(entry_text.get())
				except ValueError:
					isFloat = False
				
				if isFloat == True:
					if float(entry_text.get()) > 0.0:
						errorLabel['text'] = ""
						
						if (accVar.get()) == "CHEQUING":
							cBalance = cBalance + float(entry_text.get())
							cBtn['text'] = "$"+str("%.2f" % cBalance)
							addToFile("C", float(entry_text.get()), note_entry.get())
							
						if (accVar.get()) == "CREDIT":
							if ccBalance + float(entry_text.get()) > ccLimit:
								errorLabel['text'] = "Transaction Exceeds Credit Limit"
							else:
								ccBalance = ccBalance + float(entry_text.get())
								if ccBalance > 0.0:
									ccBtn['fg'] = 'red'
									ccBtn['activeforeground'] = 'red'
								else:
									ccBtn['fg'] = 'green'
									ccBtn['activeforeground'] = 'green'
								ccBtn['text'] = "$"+str("%.2f" % ccBalance)
								addToFile("CC", float(entry_text.get()), note_entry.get())
								
						if (accVar.get()) == "SAVINGS":
							sBalance = sBalance + float(entry_text.get())
							sBtn['text'] = "$"+str("%.2f" % sBalance)
							addToFile("S", float(entry_text.get()), note_entry.get())
					else:
						errorLabel['text'] = "Please Enter an Amount Greater Than $0.00"
				else:
					errorLabel['text'] = "Please Enter a Valid Numerical Amount"
		
		def MinusClick():
			global cBalance, ccBalance, sBalance
			isFloat = True
			
			if accVar.get() == "(Account)":
				errorLabel['text'] = "Please Choose an Account"
			elif note_entry.get() == "(Note)" or note_entry.get().isspace() or not note_entry.get():
				errorLabel['text'] = "Please Choose or Write a Note"
			else:
				try:
					float(entry_text.get())
				except ValueError:
					isFloat = False
				
				if isFloat == True:
					if float(entry_text.get()) > 0.0:
						errorLabel['text'] = ""
						if (accVar.get()) == "CHEQUING":
							if cBalance - float(entry_text.get()) < 0.0:
								errorLabel['text'] = "Not Enough Money in Chequing"
							else:
								cBalance = cBalance - float(entry_text.get())
								cBtn['text'] = "$"+str("%.2f" % cBalance)
								addToFile("C", -1*float(entry_text.get()), note_entry.get())
								
						if (accVar.get()) == "CREDIT":
							if ccBalance - float(entry_text.get()) < 0.0:
								errorLabel['text'] = "No Sufficient Outstanding Debt"
							else:
								ccBalance = ccBalance - float(entry_text.get())
								if ccBalance > 0.0:
									ccBtn['fg'] = 'red'
									ccBtn['activeforeground'] = 'red'
								else:
									ccBtn['fg'] = 'green'
									ccBtn['activeforeground'] = 'green'
								ccBtn['text'] = "$"+str("%.2f" % ccBalance)
								addToFile("CC", -1*float(entry_text.get()), note_entry.get())
								
						if (accVar.get()) == "SAVINGS":
							if sBalance - float(entry_text.get()) < 0.0:
								errorLabel['text'] = "Not Enough Money in Savings"
							else:
								sBalance = sBalance - float(entry_text.get())
								sBtn['text'] = "$"+str("%.2f" % sBalance)
								addToFile("S", -1*float(entry_text.get()), note_entry.get())
					else:
						errorLabel['text'] = "Please Enter an Amount Greater Than $0.00"
				else:
					errorLabel['text'] = "Please Enter a Valid Numerical Amount"
		
		ePlus = tk.Button(self, text="+", font=BOLD_FONT, fg='green', activeforeground='green', width=2, command=PlusClick)
		ePlus.grid(row=4, column=3, columnspan=43, sticky='e')
		eMinus = tk.Button(self, text="-", font=BOLD_FONT, fg='red', activeforeground='red', width=2, command=MinusClick)
		eMinus.grid(row=4, column=3, columnspan=49, sticky='e')
		
		def OptionChoice(choice):
			if choice == 'CREDIT':
				ePlus['fg'] = 'red'
				ePlus['activeforeground'] = 'red'
				eMinus['fg'] = 'green'
				eMinus['activeforeground'] = 'green'
			else:
				ePlus['fg'] = 'green'
				ePlus['activeforeground'] = 'green'
				eMinus['fg'] = 'red'
				eMinus['activeforeground'] = 'red'
				
		#OptionMenu for account type
		accVar = tk.StringVar(self)
		accVar.set("(Account)")
		accOption = tk.OptionMenu(self, accVar, "CHEQUING", "CREDIT", "SAVINGS", command=OptionChoice).grid(row=4, column=0, columnspan=18, sticky='ew')
		
		#OptionMenu for note type, takes inputs from and outputs to a text file
		for i in range(len(nOptions)):
			if "\n" in nOptions[i]:
				nOptions[i] = nOptions[i].replace("\n", "")
				
		note_entry = AutoComplete(nOptions, self, width=10)
		note_entry.grid(row=4, column=18, columnspan=16, sticky='ew')
		
		note_entry.bind('<Button-1>', noteDelete) #clicking inside the note input will call noteDelete and delete the current text

#general class for the three frame objects used for account types
class Page(tk.Frame):
	def __init__(self, master, name, abbr, balance):
		tk.Frame.__init__(self, master)
		
		root.geometry('702x350')
		root.resizable(width=False, height=False)
		root.configure(bg='white')
		Page.configure(self, bg='white')
		
		title = tk.Label(self, text=(name+" Account Summary"), font=LARGE_FONT, bg='white', pady=8)
		title.grid(row=0, column=24)
		
		backBtn = tk.Button(self, text="Home", width=10, bg='white', bd=1, relief='ridge', command=lambda: showFrame(HomePage(root)))
		backBtn.grid(row=2, column=24)
		
		xPlot, yPlot, tactList = [], [], []
		
		recFile = open(dp+'records.txt', 'r')
		recVals = recFile.read().split('\n')
		recFile.close()
		
		for i in range(len(recVals)-1):
			recVals[i] = recVals[i].split(', ')
			if recVals[i][0] == abbr:
				xPlot.append(recVals[i][3]) #append dates
				yPlot.append(float(recVals[i][1])) #append values
				tactList.append(recVals[i][1:]) #append whole transaction
		
		f = Figure(figsize=(5,3), dpi = 100) #create figure object
		f.set_tight_layout(True)
		a = f.add_subplot(111) #1x1 grid, first subplot
		a.grid() #draw a grid onto the figure
		a.set_xlabel("Transaction Dates (One Day Intervals)", style='italic', fontsize=9)
		a.set_ylabel("Balance ($)", style='italic', fontsize=9)
		a.tick_params(labelsize='8') #font size of ticks
		
		i = 0
		while i < len(xPlot):
			if len(xPlot) > i+1 and (xPlot[i] == xPlot[i+1]):
				yPlot[i] += yPlot[i+1] #add up all the values on the same date
				del xPlot[i+1]
				del yPlot[i+1]
				if i != 0:
					i-=1
			else:
				i+=1
				
		addList=[]
		#each index of yPlot is the sum of its previous indices to be able to graph the overall bank account balances at the time of transaction
		for i in range(1, len(yPlot)+1):
			addList.append(sum(yPlot[:i]))
		yPlot = addList
		
		graphCol = "-g"
		if abbr == 'CC':
			if len(yPlot) > 0:
				if yPlot[-1] > 0:		
					graphCol = "-r"
		else:
			if len(yPlot) > 1:
				if yPlot[-1] < yPlot[-2]:
					graphCol = "-r"
		
		#keep only first and last date entry as date formats
		xtickList = []
		if len(xPlot) > 0:
			xtickList.append(xPlot[0])
			for i in xPlot:
				if i != xPlot[0] and i != xPlot[-1]:
					xtickList.append('') #replace other entries with a blank
			xtickList.append(xPlot[-1])
			
		a.set_xticklabels(xtickList)
		a.plot(xPlot, yPlot, graphCol, marker='.', markersize='2')
		
		canvas = FigureCanvasTkAgg(f, self) #create the plot canvas
		canvas.draw()
		canvas.get_tk_widget().grid(row=3, column=0, columnspan=30, rowspan=20)
		
		spacer = tk.Label(self, text=" ", bg='white') #column spacer for formatting
		spacer.grid(row=0, column=31)
		
		tactTitle = tk.Label(self, text="Transactions", font=BOLD_FONT, bg='white')
		tactTitle.grid(row=3, column=32)
		
		tactLb = tk.Listbox(self, width=30, height=14, borderwidth=0)
		tactLb.grid(row=4, column=32, columnspan=30, rowspan=40, sticky='n')
		
		#add the account transactions to their respective listboxes
		lbEntry = ""
		i=0
		for i in range(len(tactList)):
			for index in tactList[i]:
				lbEntry += index + ", "
			if float(tactList[i][0]) > 0.0:
				tactLb.insert('end', "+$"+lbEntry[:-2])
				if abbr == 'CC':
					tactLb.itemconfig(i, foreground='red')
				else:
					tactLb.itemconfig(i, foreground='green')
			else:
				tactLb.insert('end', "-$"+lbEntry[1:-2])
				if abbr == 'CC':
					tactLb.itemconfig(i, foreground='green')
				else:
					tactLb.itemconfig(i, foreground='red')
			lbEntry = ""
			i+=1

if __name__ == '__main__': #code only executed to run as a program not when simply imported as a module
	root = tk.Tk()
	root.wm_title("Assets 1.4")
	
	imgIcon = tk.PhotoImage(file=imgp)
	root.tk.call('wm', 'iconphoto', root._w, imgIcon)
	
	showFrame(HomePage(root)) #start with HomePage
	root.mainloop()