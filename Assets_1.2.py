#Assets 2018 created by Alex Moica

import tkinter as tk
import os
import re
import sys
import time

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

baseVals = balFile.readlines()

if os.path.exists(dp+'records.txt'):
	recFile = open(dp+'records.txt', 'r')
else:
	recFile = open(dp+'records.txt', 'w')
	recFile.close
	recFile = open(dp+'balance.txt', 'r')

recVals = recFile.read().split('\n')

optionFile = fileOpen(dp+'note options.txt', 'r')

nOptions = []

try:
	for line in optionFile.readlines():
		nOptions.append(line)
except:
	os.execl(sys.executable, sys.executable, *sys.argv)
	
balFile.close()
recFile.close()
optionFile.close()

CxPlot, CCxPlot, SxPlot = [], [], []
CyPlot, CCyPlot, SyPlot = [], [], []

for i in range(len(recVals)-1):
	recVals[i] = recVals[i].split(', ')
	if recVals[i][0] == 'C':
		CxPlot.append(recVals[i][3])
		CyPlot.append(float(recVals[i][1]))
	elif recVals[i][0] == 'CC':
		CCxPlot.append(recVals[i][3])
		CCyPlot.append(float(recVals[i][1]))
	else:
		SxPlot.append(recVals[i][3])
		SyPlot.append(float(recVals[i][1]))
		
cBalance = float("%.2f" % float(baseVals[0]))
ccBalance = float("%.2f" % float(baseVals[1]))
sBalance = float("%.2f" % float(baseVals[2]))
ccLimit = 1000.00

if ccBalance > 0.0:
	balCol = 'red'
else:
	balCol = 'green'

def entryAdd(plotList):
		cSum = 0
		for i in plotList:
			cSum += i
			yield cSum
			
class Assets(tk.Tk):

	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "Assets 1.2")
		
		container = tk.Frame(self)
		
		container.pack(side='top', fill='both', expand=True)
		
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		#Initialize all the pages in the app
		for page in (HomePage, CPage, CCPage, SPage):
			frame = page(container, self)
			self.frames[page] = frame
			frame.grid(row=0, column=0, sticky='nsew')
		
		self.show_frame(HomePage)
	
	#Show the container based on the frame called
	def show_frame(self, container):
		frame = self.frames[container]
		frame.tkraise()

class AutoComplete(tk.Entry):
	def __init__(self, entries, *args, **kwargs):
		tk.Entry.__init__(self, *args, **kwargs)
		self.entries = entries
		self.var = self['textvariable']
		if self.var == '':
			self.var = self['textvariable'] = tk.StringVar()
		
		self.var.set("(Note)")
		self.var.trace('w', self.update)
		self.bind('<Return>', self.select)
		self.bind('<Up>', self.up)
		self.bind('<Down>', self.down)
		
		self.lb_up = False
		self.lb = tk.Listbox()
		
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
			if self.lb.curselection() == () or self.lb.curselection() == (0,):
				index = str(self.lb.size()-1)
			else:
				index = str(int(self.lb.curselection()[0])-1)
			
			if index != '0' and index != str(self.lb.size()-1):
				self.lb.selection_clear(first=str(int(index)+1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)-1)
			elif index == str(self.lb.size()-1):
				self.lb.selection_clear(first='0')
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)-1)
			else:
				self.lb.selection_clear(first=str(int(index)+1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(self.lb.size()-1))
		
	def down(self, event):
		if self.lb_up:
			if self.lb.curselection() == () or self.lb.curselection() == (self.lb.size()-1,):
				index = '0'
			else:
				index = str(int(self.lb.curselection()[0])+1)
				
			if index != '0' and index != str(self.lb.size()-1):
				self.lb.selection_clear(first=str(int(index)-1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)+1)
			elif index == str(self.lb.size()-1):
				self.lb.selection_clear(first=str(int(index)-1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = '0'
			else:
				self.lb.selection_clear(first=str(self.lb.size()-1))
				self.lb.selection_set(first=index)
				self.lb.activate(index)
				index = str(int(index)+1)
				
	def compare(self):
		pattern = re.compile('.*' + self.var.get().upper() + '.*')
		return [i for i in self.entries if re.match(pattern, i)]
				
class HomePage(tk.Frame):
	
	def __init__(self, master, controller):			
		tk.Frame.__init__(self, master)
		
		x = True
		for j in range(51):
			x = not x
			if x == True:
				tk.Label(self, bg='#edef58').grid(row=0, column=j)
			else:
				tk.Label(self, bg='#000000').grid(row=0, column=j)
				
		accLbl = tk.Label(self, text="Accounts", font=LARGE_FONT).grid(row=1, column=0, columnspan=12, sticky='ew')

		#Chequing Objects
		cLbl = tk.Label(self, text="Chequing").grid(row=2, column=0, columnspan=10, sticky='w')
		cdLbl = tk.Label(self, text=". "*29).grid(row=2, column=1, columnspan=38, sticky='e')
		cBtn = tk.Button(self, text="$"+str(cBalance), fg='green', activeforeground='green', width=10, command=lambda: controller.show_frame(CPage))
		cBtn.grid(row=2, column=2, columnspan=50, sticky='e')
		
		#Credit Objects
		ccLbl = tk.Label(self, text="Credit").grid(row=3, column=0, columnspan=10, sticky='w')
		ccdLbl = tk.Label(self, text=". "*32).grid(row=3, column=1, columnspan=38, sticky='e')
		ccBtn = tk.Button(self, text="$"+str(ccBalance), fg=balCol, activeforeground=balCol, width=10, command=lambda: controller.show_frame(CCPage))
		ccBtn.grid(row=3, column=2, columnspan=50, sticky='e')
		
		#Savings Objects
		sLbl = tk.Label(self, text="Savings").grid(row=4, column=0, columnspan=10, sticky='w')
		sdLbl = tk.Label(self, text=". "*31).grid(row=4, column=1, columnspan=38, sticky='e')
		sBtn = tk.Button(self, text="$"+str(sBalance), fg='green', activeforeground='green', width=10, command=lambda: controller.show_frame(SPage))
		sBtn.grid(row=4, column=2, columnspan=50, sticky='e')
		
		#Function to delete text on click inside entry fields
		def amountDelete(event):
			entry_widget.delete(0, 'end')
			
		def noteDelete(event):
			if note_entry.get() != '':
				note_entry.lb_up = True
			else:
				note_entry.lb_up = False
				
			note_entry.delete(0, 'end')
		
		#Input Objects
		eDollar = tk.Label(self, text="$", font=BOLD_FONT).grid(row=5, column=1, columnspan=36, sticky='e')
		entry_text = tk.StringVar()
		entry_text.set("0.00")
		
		entry_widget= tk.Entry(self, relief='flat', width=5, textvariable=entry_text)
		entry_widget.grid(row=5, column=2, columnspan=40, sticky='e')
		entry_widget.bind('<Button-1>', amountDelete)

		errorLabel = tk.Label(self, text="", font=BOLD_FONT, fg='red')
		errorLabel.grid(row=6, column=0, columnspan=70, sticky='w')
			
		#Add new records and balances to their respective files
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
			
			print()
		
		def PlusClick(): #TODO on click check if the text exists in the note options file already
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
							if ccBalance + float(entry_text.get()) > 1000.00:
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
		
		def MinusClick(): #TODO on click check if the text exists in the note options file already
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
		ePlus.grid(row=5, column=3, columnspan=44, sticky='e')
		eMinus = tk.Button(self, text="-", font=BOLD_FONT, fg='red', activeforeground='red', width=2, command=MinusClick)
		eMinus.grid(row=5, column=3, columnspan=49, sticky='e')
		
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
				
		#ObjectMenu for account type
		accVar = tk.StringVar(self)
		accVar.set("(Account)")
		accOption = tk.OptionMenu(self, accVar, "CHEQUING", "CREDIT", "SAVINGS", command=OptionChoice).grid(row=5, column=0, columnspan=18, sticky='ew')
		
		#ObjectMenu for note type, takes inputs from and outputs to a text file
		for i in range(len(nOptions)):
			if "\n" in nOptions[i]:
				nOptions[i] = nOptions[i].replace("\n", "")
				
		note_entry = AutoComplete(nOptions, self, width=10)
		note_entry.grid(row=5, column=18, columnspan=16, sticky='ew')
		
		note_entry.bind('<Button-1>', noteDelete)

class CPage(tk.Frame):
	
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		
		cLbl = tk.Label(self, text="Chequing Account Summary", font=LARGE_FONT)
		cLbl.pack(pady=10, padx=10)
		
		backBtn = tk.Button(self, text="Accounts", command=lambda: controller.show_frame(HomePage))
		backBtn.pack()
		
		global CxPlot, CyPlot
		
		f = Figure(figsize=(7,3), dpi = 100)
		f.set_tight_layout(True)
		a = f.add_subplot(111)
		a.grid()
		a.set_xlabel("Transaction Dates (One Day Intervals)", style='italic', fontsize=9)
		a.set_ylabel("Balance ($)", style='italic', fontsize=9)
		a.tick_params(labelsize='8')
		
		i = 0
		while i < len(CxPlot):
			if len(CxPlot) > i+1 and (CxPlot[i] == CxPlot[i+1]):
				CyPlot[i] += CyPlot[i+1]
				del CxPlot[i+1]
				del CyPlot[i+1]
				if i != 0:
					i-=1
			else:
				i+=1
		
		newCyPlot = []
		for i in (entryAdd(CyPlot)):
			newCyPlot.append(i)
		
		CyPlot = newCyPlot
		
		graphCol = "-g"
		if len(CyPlot) > 1:
			if CyPlot[-1] < CyPlot[-2]:
				graphCol = "-r"
		
		fml = []
		if len(CxPlot) > 2:
			for i in CxPlot:
				if i == CxPlot[0] or i == CxPlot[-1]:
					fml.append(i)
				else:
					fml.append(CxPlot.index(i))
		
		xtickList = []
		if len(CxPlot) > 0:
			xtickList.append(CxPlot[0])
			for i in CxPlot:
				if i != CxPlot[0] and i != CxPlot[-1]:
					xtickList.append('')
			xtickList.append(CxPlot[-1])
			
		a.set_xticklabels(xtickList)
		
		if len(CxPlot) > 2:
			a.plot(fml, CyPlot, graphCol, marker='.', markersize='2')
		else:
			a.plot(CxPlot, CyPlot, graphCol, marker='.', markersize='2')
		
		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
	
class CCPage(tk.Frame):
	
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		
		ccLbl = tk.Label(self, text="Credit Account Summary", font=LARGE_FONT)
		ccLbl.pack(pady=10, padx=10)
		
		backBtn = tk.Button(self, text="Accounts", command=lambda: controller.show_frame(HomePage))
		backBtn.pack()
		
		global CCxPlot, CCyPlot
		
		f = Figure(figsize=(7,3), dpi = 100)
		f.set_tight_layout(True)
		a = f.add_subplot(111)
		a.grid()
		a.set_xlabel("Transaction Dates (One Day Intervals)", style='italic', fontsize=9)
		a.set_ylabel("Balance ($)", style='italic', fontsize=9)
		a.tick_params(labelsize='8')
		
		i = 0
		while i < len(CCxPlot):
			if len(CCxPlot) > i+1 and (CCxPlot[i] == CCxPlot[i+1]):
				CCyPlot[i] += CCyPlot[i+1]
				del CCxPlot[i+1]
				del CCyPlot[i+1]
				if i != 0:
					i-=1
			else:
				i+=1
		
		newCCyPlot = []
		for i in (entryAdd(CCyPlot)):
			newCCyPlot.append(i)
		
		CCyPlot = newCCyPlot
		
		graphCol = "-g"
		if len(CCyPlot) > 0:
			if CCyPlot[-1] > 0:		
				graphCol = "-r"
		
		fml = []
		if len(CCxPlot) > 2:
			for i in CCxPlot:
				if i == CCxPlot[0] or i == CCxPlot[-1]:
					fml.append(i)
				else:
					fml.append(CCxPlot.index(i))
		
		xtickList = []
		if len(CCxPlot) > 0:
			xtickList.append(CCxPlot[0])
			for i in CCxPlot:
				if i != CCxPlot[0] and i != CCxPlot[-1]:
					xtickList.append('')
			xtickList.append(CCxPlot[-1])
			
		a.set_xticklabels(xtickList)
		
		if len(CCxPlot) > 2:
			a.plot(fml, CCyPlot, graphCol, marker='.', markersize='2')
		else:
			a.plot(CCxPlot, CCyPlot, graphCol, marker='.', markersize='2')
		
		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		
class SPage(tk.Frame):
	
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		
		sLbl = tk.Label(self, text="Savings Account Summary", font=LARGE_FONT)
		sLbl.pack(pady=10, padx=10)
		
		backBtn = tk.Button(self, text="Accounts", command=lambda: controller.show_frame(HomePage))
		backBtn.pack()

		global SxPlot, SyPlot
		
		f = Figure(figsize=(7,3), dpi = 100)
		f.set_tight_layout(True)
		a = f.add_subplot(111)
		a.grid()
		a.set_xlabel("Transaction Dates (One Day Intervals)", style='italic', fontsize=9)
		a.set_ylabel("Balance ($)", style='italic', fontsize=9)
		a.tick_params(labelsize='8')
		
		i = 0
		while i < len(SxPlot):
			if len(SxPlot) > i+1 and (SxPlot[i] == SxPlot[i+1]):
				SyPlot[i] += SyPlot[i+1]
				del SxPlot[i+1]
				del SyPlot[i+1]
				if i != 0:
					i-=1
			else:
				i+=1
		
		newSyPlot = []
		for i in (entryAdd(SyPlot)):
			newSyPlot.append(i)
		
		SyPlot = newSyPlot
		
		graphCol = "-g"
		if len(SyPlot) > 1:
			if SyPlot[-1] < SyPlot[-2]:
				graphCol = "-r"
		
		fml = []
		if len(SxPlot) > 2:
			for i in SxPlot:
				if i == SxPlot[0] or i == SxPlot[-1]:
					fml.append(i)
				else:
					fml.append(SxPlot.index(i))
		
		xtickList = []
		if len(SxPlot) > 0:
			xtickList.append(SxPlot[0])
			for i in SxPlot:
				if i != SxPlot[0] and i != SxPlot[-1]:
					xtickList.append('')
			xtickList.append(SxPlot[-1])
			
		a.set_xticklabels(xtickList)
		
		if len(SxPlot) > 2:
			a.plot(fml, SyPlot, graphCol, marker='.', markersize='2')
		else:
			a.plot(SxPlot, SyPlot, graphCol, marker='.', markersize='2')
		
		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		
root = Assets()

imgIcon = tk.PhotoImage(file=dp+'AssetsIcon.ico')
root.tk.call('wm', 'iconphoto', root._w, imgIcon)
root.geometry("306x306")

root.resizable(width=False, height=False)

root.mainloop()