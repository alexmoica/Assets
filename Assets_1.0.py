#Assets 2018 created by Alex Moica

import tkinter as tk
from tkinter import simpledialog
import os
import sys

LARGE_FONT = ('Verdana 10 underline')
BOLD_FONT = ('Verdana 9 bold')

dp = os.path.join(os.path.dirname(__file__),'')

def fileOpen(path, type):
	if os.path.exists(path):
		fileName = open(path, type)
		return fileName
	else:
		fileName = open(path, 'w')
		return fileName
		
if os.path.exists(dp+'balance.txt'):
	balFile = open(dp+'balance.txt', 'r')
else:
	balFile = open(dp+'balance.txt', 'w')
	balFile.write("0.0\n0.0\n0.0")
	balFile.close
	balFile = open(dp+'balance.txt', 'r')

optionFile = fileOpen(dp+'note options.txt', 'r')

baseVals = balFile.readlines()

recFile = fileOpen(dp+'records.txt', 'r')
noteFile = fileOpen(dp+'notes.txt', 'r')

nOptions = ['New...']

try:
	for line in optionFile.readlines():
		nOptions.append(line)
except:
	os.execl(sys.executable, sys.executable, *sys.argv)

balFile.close()
recFile.close()
noteFile.close()
optionFile.close()

cBalance = float("%.2f" % float(baseVals[0]))
ccBalance = float("%.2f" % float(baseVals[1]))
sBalance = float("%.2f" % float(baseVals[2]))
ccLimit = 1000.00

if ccBalance > 0.0:
	balCol = 'red'
else:
	balCol = 'green'

class Assets(tk.Tk):

	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		
		tk.Tk.wm_title(self, "Assets 1.0")
		
		container = tk.Frame(self)
		
		container.pack(side='top', fill='both', expand=True)
		
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		#Initialize all the pages in the app
		frame = HomePage(container, self)
		self.frames[HomePage] = frame
		frame.grid(row=0, column=0, sticky='nsew')
		
		self.show_frame(HomePage)
	
	#Show the container based on the frame called
	def show_frame(self, container):
		frame = self.frames[container]
		frame.tkraise()
		
class HomePage(tk.Frame):
	
	def __init__(self, master, controller):			
		tk.Frame.__init__(self, master)
		
		x = True
		for j in range(60):
			x = not x
			if x == True:
				tk.Label(self, bg='black').grid(row=0, column=j)
			else:
				tk.Label(self, bg='white').grid(row=0, column=j)
				
		accLbl = tk.Label(self, text="Accounts", font=LARGE_FONT).grid(row=1, column=0, columnspan=10, sticky='ew')

		#Chequing Objects
		cLbl = tk.Label(self, text="Chequing").grid(row=2, column=0, columnspan=10, sticky='w')
		cdLbl = tk.Label(self, text=". "*30).grid(row=2, column=1, columnspan=38, sticky='e')
		cBtn = tk.Button(self, text="$"+str(cBalance), fg='green', width=10)
		cBtn.grid(row=2, column=2, columnspan=50, sticky='e')
		
		#Credit Objects
		ccLbl = tk.Label(self, text="Credit").grid(row=3, column=0, columnspan=10, sticky='w')
		ccdLbl = tk.Label(self, text=". "*33).grid(row=3, column=1, columnspan=38, sticky='e')
		ccBtn = tk.Button(self, text="$"+str(ccBalance), fg=balCol, width=10)
		ccBtn.grid(row=3, column=2, columnspan=50, sticky='e')
		
		#Savings Objects
		sLbl = tk.Label(self, text="Savings").grid(row=4, column=0, columnspan=10, sticky='w')
		sdLbl = tk.Label(self, text=". "*32).grid(row=4, column=1, columnspan=38, sticky='e')
		sBtn = tk.Button(self, text="$"+str(sBalance), fg='green', width=10)
		sBtn.grid(row=4, column=2, columnspan=50, sticky='e')
		
		#Function to delete text on click inside an entry field
		def deleteSearch(event):
			entry_widget.delete(0, 'end')
		
		#Input Objects
		eDollar = tk.Label(self, text="$", font=BOLD_FONT).grid(row=5, column=1, columnspan=35, sticky='e')
		entry_text = tk.StringVar()
		entry_text.set("0.00")
		
		entry_widget= tk.Entry(self, relief='flat', width=6, textvariable=entry_text)
		entry_widget.grid(row=5, column=2, columnspan=40, sticky='e')
		entry_widget.bind('<Button-1>', deleteSearch)

		errorLabel = tk.Label(self, text="", font=BOLD_FONT, fg='red')
		errorLabel.grid(row=6, column=0, columnspan=70, sticky='w')
			
		#Add new records and balances to their respective files
		def addToFile(val, note):
			global cBalance, ccBalance, sBalance, nOptions
			
			balF = open(dp+'balance.txt', 'w')
			balF.write(str(cBalance)+"\n"+str(ccBalance)+"\n"+str(sBalance)+"\n")
			balF.close()
			
			recF = open(dp+'records.txt', 'a')
			recF.write(str(val)+"\n")
			recF.close()
			
			noF = open(dp+'notes.txt', 'a')
			noF.write(note.capitalize()+"\n")
			noF.close()
			
			opF = open(dp+'note options.txt', 'r')
			nOptions = opF.readlines()
			opF.close()
			
			opF = open(dp+'note options.txt', 'a')
			if note+"\n" not in nOptions:
				opF.write(note+"\n")
			opF.close()
		
		def PlusClick():
			global cBalance, ccBalance, sBalance, ccLimit
			isFloat = True
			
			if accVar.get() == "(Account)":
				errorLabel['text'] = "Please Choose an Account"
			elif noteVar.get() == "(Note)":
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
							addToFile(("C"+" +"+str(entry_text.get())), noteVar.get())
							
						if (accVar.get()) == "CREDIT":
							if ccBalance + float(entry_text.get()) > 1000.00:
								errorLabel['text'] = "Transaction Exceeds Credit Limit"
							else:
								ccBalance = ccBalance + float(entry_text.get())
								if ccBalance > 0.0:
									ccBtn['fg'] = 'red'
								else:
									ccBtn['fg'] = 'green'
								ccBtn['text'] = "$"+str("%.2f" % ccBalance)
								addToFile(("CC"+" +"+str(entry_text.get())), noteVar.get())
								
						if (accVar.get()) == "SAVINGS":
							sBalance = sBalance + float(entry_text.get())
							sBtn['text'] = "$"+str("%.2f" % sBalance)
							addToFile(("S"+" +"+str(entry_text.get())), noteVar.get())
							
					else:
						errorLabel['text'] = "Please Enter an Amount Greater Than $0.00"
				else:
					errorLabel['text'] = "Please Enter a Valid Numerical Amount"
		
		def MinusClick():
			global cBalance, ccBalance, sBalance
			isFloat = True
			
			if accVar.get() == "(Account)":
				errorLabel['text'] = "Please Choose an Account"
			elif noteVar.get() == "(Note)":
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
								addToFile(("C"+" -"+str(entry_text.get())), noteVar.get())
								
						if (accVar.get()) == "CREDIT":
							if ccBalance - float(entry_text.get()) < 0.0:
								errorLabel['text'] = "No Sufficient Outstanding Debt"
							else:
								ccBalance = ccBalance - float(entry_text.get())
								if ccBalance > 0.0:
									ccBtn['fg'] = 'red'
								else:
									ccBtn['fg'] = 'green'
								ccBtn['text'] = "$"+str("%.2f" % ccBalance)
								addToFile(("CC"+" -"+str(entry_text.get())), noteVar.get())
								
						if (accVar.get()) == "SAVINGS":
							if sBalance - float(entry_text.get()) < 0.0:
								errorLabel['text'] = "Not Enough Money in Savings"
							else:
								sBalance = sBalance - float(entry_text.get())
								sBtn['text'] = "$"+str("%.2f" % sBalance)
								addToFile(("S"+" -"+str(entry_text.get())), noteVar.get())
					else:
						errorLabel['text'] = "Please Enter an Amount Greater Than $0.00"
				else:
					errorLabel['text'] = "Please Enter a Valid Numerical Amount"
		
		ePlus = tk.Button(self, text="+", font=BOLD_FONT, fg='green', width=2, command=PlusClick)
		ePlus.grid(row=5, column=3, columnspan=44, sticky='e')
		eMinus = tk.Button(self, text="-", font=BOLD_FONT, fg='red', width=2, command=MinusClick)
		eMinus.grid(row=5, column=3, columnspan=49, sticky='e')
		
		def OptionChoice(choice):
			if choice == 'CREDIT':
				ePlus['fg'] = 'red'
				eMinus['fg'] = 'green'
			else:
				ePlus['fg'] = 'green'
				eMinus['fg'] = 'red'
				
		def NotesChoice(choice):
			if choice == OPTIONS[0]:
				newNote = simpledialog.askstring("New Note", "Please write a note:")
				OPTIONS.append(newNote.capitalize())
				
				optionName = OPTIONS[-1]
				if len(optionName) > 6:
					optionName = OPTIONS[-1][0:6]+"..."
					
				noteVar.set(optionName)
				
				noteOption['menu'].add_command(label=optionName, command=tk._setit(noteVar, optionName))
			
		#ObjectMenu for account type
		accVar = tk.StringVar(self)
		accVar.set("(Account)")
		accOption = tk.OptionMenu(self, accVar, "CHEQUING", "CREDIT", "SAVINGS", command=OptionChoice).grid(row=5, column=0, columnspan=17, sticky='ew')
		
		#ObjectMenu for note type, takes inputs from and outputs to a text file
		noteVar = tk.StringVar(self)
		noteVar.set("(Note)")
		for i in range(len(nOptions)):
			if "\n" in nOptions[i]:
				nOptions[i] = nOptions[i].replace("\n", "")
				
		OPTIONS = nOptions
		noteOption = tk.OptionMenu(self, noteVar, *OPTIONS, command=NotesChoice)
		noteOption.grid(row=5, column=17, columnspan=16, sticky='ew')
		
root = Assets()

imgIcon = tk.PhotoImage(file=dp+'AssetsIcon.ico')
root.tk.call('wm', 'iconphoto', root._w, imgIcon)

root.resizable(width=False, height=False)

root.mainloop()