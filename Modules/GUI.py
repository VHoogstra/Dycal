import json
import os
import queue
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from pprint import pprint

from Modules.ConfigLand import ConfigLand
from Modules.Dyflexis import Dyflexis
from Modules.Logger import Logger
from Modules.ICS import ICS


class Gui(tk.Frame):
    zaantheaterColor = "#7a4689"
    driver = None
    calendar = None
    eventDate = {}
    dyflexisMessage = "test "
    minChromeWidth = 1027

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W, padx=10, pady=10)
        self.config = ConfigLand()

        self.master.title('Dyflexis -> Google calendar')
        self.master.configure(background=self.zaantheaterColor)

        w = 470  # width for the Tk root
        h = 600  # height for the Tk root

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        x = ws / 3
        if x < self.minChromeWidth:
            x = self.minChromeWidth
        y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master.grid_propagate(0)

        # nee resize is niet toegestaan
        self.master.resizable(False, False)
        self.createWidgets()

        self.master.lift()

    def createWidgets(self):
        self.configure(background=self.zaantheaterColor)
        self.rowconfigure(1, minsize=20)
        #4, tussen dyflexis config en resultaat
        self.rowconfigure(4, minsize=15)
        #tussen dyflexis en ics
        self.rowconfigure(6, minsize=40)
        self.master.rowconfigure(7, minsize=20)

        self.configLoad = tk.Button(self, text='Laad uit config', command=self.loadConfig, fg='white', bg='black')
        self.configLoad.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.save = tk.Button(self, text='save naar config', command=self.saveConfig, fg='white', bg='black')
        self.save.grid(row=0, column=3, sticky=tk.N + tk.S + tk.W + tk.E)

#row 3
        label = tk.Label(text='Dyflexis', fg="white", bg=self.zaantheaterColor, width=10, height=1, )
        dyflexisFrame = tk.LabelFrame(self, labelwidget=label, bg=self.zaantheaterColor, padx=10, pady=10)
        dyflexisFrame.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW)
        dyflexisFrame.rowconfigure(3,minsize=10)
        self.createLabel(text="username", anchor=dyflexisFrame).grid(row=1, column=0)
        self.dyflexisUsername = self.createEntry(anchor=dyflexisFrame)
        self.dyflexisUsername.grid(row=1, column=1)

        self.createLabel(text="Password", anchor=dyflexisFrame).grid(row=2, column=0)
        self.dyflexisPassword = self.createEntry(anchor=dyflexisFrame)
        self.dyflexisPassword.grid(row=2, column=1)

        tk.Button(dyflexisFrame, text='Dyflexis uitlezen', fg='white', bg='black',
                  command=self.dyflexisRead).grid(row=4, column=0,columnspan=2)

        dyflexisLabel = tk.Label(text='Dyflexis resultaat', fg="white", bg=self.zaantheaterColor, width=15, height=1, )
        dyflexisResultaatFrame = tk.LabelFrame(self, labelwidget=dyflexisLabel, bg=self.zaantheaterColor, padx=10,
                                               pady=10)
        dyflexisResultaatFrame.columnconfigure(0, weight=1)
        dyflexisResultaatFrame.grid(row=5, column=0, columnspan=4, sticky=tk.W + tk.N + tk.E + tk.S)

        self.dyflexisProgressBarValue = tk.IntVar()
        self.dyflexisProgressBar = ttk.Progressbar(dyflexisResultaatFrame, mode='determinate', maximum=101,
                                                   variable=self.dyflexisProgressBarValue)
        self.dyflexisProgressBar.grid(row=0, column=0, sticky=tk.E + tk.W)
        self.dyflexisMessage = tk.Message(dyflexisResultaatFrame, text="Nog geen informatie", fg='white', bg='red',
                                          justify=tk.LEFT,
                                          aspect=500,
                                          width=300)
        self.dyflexisMessage.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        GoogleLabel = tk.Label(text='ICS configuratie', fg="white", bg=self.zaantheaterColor, width=15, height=1, )
        googleResultaatFrame = tk.LabelFrame(self, labelwidget=GoogleLabel, bg=self.zaantheaterColor, padx=10,
                                             pady=10)
        googleResultaatFrame.grid(row=8, column=0, columnspan=4, sticky=tk.W + tk.N + tk.E + tk.S)
        googleResultaatFrame.columnconfigure(0, weight=1)
        self.createLabel(text="ics url", anchor=googleResultaatFrame).grid(row=1, column=0)
        self.icsUrl = self.createEntry(anchor=googleResultaatFrame)
        self.icsUrl.grid(row=1, column=1)

        self.createLabel(text="of ", anchor=googleResultaatFrame).grid(row=2, column=0)

        tk.Button(googleResultaatFrame, text='Laad ISC data uit bestand', command=self.uploadICS, fg='white',
                  bg='black').grid(row=2, column=1)
        tk.Button(googleResultaatFrame, text='Laad ICS data uit URL', fg='white', bg='black',
                  command=self.loadICS).grid(row=4, column=0)

        tk.Message(googleResultaatFrame, text='nog geen informatie', fg='white', bg='red', justify=tk.LEFT).grid(row=4,
                                                                                                                 column=0,
                                                                                                                 columnspan=2,
                                                                                                                 sticky=tk.N + tk.S + tk.W + tk.E)
        tk.Button(self, text='Genereer ICS', fg='white', bg='black', command=self.generateICS).grid(row=9, column=3)

    def createLabel(self, text, anchor=None):
        if anchor == None:
            anchor = self
        return tk.Label(
            anchor,
            text=text,
            fg="white",
            bg="black",
            width=10,
            height=1,
        )

    def createEntry(self, anchor=None, variable=None):
        if anchor == None:
            anchor = self
        return tk.Entry(
            anchor,
            fg="white",
            bg="black",
            highlightbackground=self.zaantheaterColor,
            width=50,
            insertbackground='red',
            highlightcolor='red',
            variable=variable
        )

    def loadConfig(self):
        self.config.loadConfig()
        self.dyflexisPassword.delete(0, 500)
        self.dyflexisPassword.insert(0, self.config.Config['dyflexis']['password'])

        self.dyflexisUsername.delete(0, 500)
        self.dyflexisUsername.insert(0, self.config.Config['dyflexis']['username'])

        self.icsUrl.delete(0, 500)
        self.icsUrl.insert(0, self.config.Config['ics']['url'])

    def saveConfig(self):
        self.config.Config['dyflexis']['password'] = self.dyflexisPassword.get()
        self.config.Config['dyflexis']['username'] = self.dyflexisUsername.get()
        self.config.Config['ics']['url'] = self.icsUrl.get()
        self.config.saveConfig()

    def updateDyflexisProgressBar(self, amount):
        if not isinstance(amount, tk.IntVar):
            temp = tk.IntVar()
            temp.set(amount)
            amount = temp
        print('updateDyflexisProgressbar ' + str(amount.get()))
        self.dyflexisProgressBarValue.set(value=amount.get())
        self.dyflexisProgressBar.update()

    def dyflexisRead(self):
        self.dyflexis = Dyflexis(self.config, self.master.winfo_screenwidth(), self.master.winfo_screenheight(),
                                 self.minChromeWidth)
        try:
            self.eventData = self.dyflexis.run(_progressbarCallback=self.updateDyflexisProgressBar)
        except Exception as e:
            Message = 'Failed to run dyflexys: %s' + repr(e)
            self.dyflexisMessage.config(text=Message, bg='red')
            raise e

        # with open('icsData.json', 'r') as fp:
        #     superValue = fp.read()
        #     self.eventData = json.loads(superValue)
        #     fp.close()

        # create the information message for the GUI
        assignments = str(self.eventData['assignments'])
        agenda = str(self.eventData['agenda'])
        events = str(self.eventData['events'])
        start_date = self.eventData['list'][0]['date']
        end_date = self.eventData['list'][len(self.eventData['list']) - 1]['date']
        Message = f"Assignments: {assignments} \nAgenda: \t{agenda} \nEvents: \t{events} \nperiode: \n{start_date} tot {end_date}"
        self.dyflexisMessage.config(text=Message, bg='green')

    def uploadICS(self):
        if self.calendar == None:
            self.calendar = ICS()
        print('uploadIcs')
        icsdata = filedialog.askopenfilename(defaultextension="ics", title="ICS bestand van uw kalender app",
                                             initialdir=os.path.expanduser('~/Downloads'))
        if icsdata is not None:
            self.calendar.connectToICS(file=icsdata)
            ##todo give feedback

    def loadICS(self):
        if self.calendar == None:
            self.calendar = ICS()
        if (self.icsUrl.get() != None):
            self.calendar.connectToICS(url=self.icsUrl.get())
        print('loadIcs')
        ##todo give feedback

    def generateICS(self):
        print('generateICS')
        if self.calendar == None:
            raise Exception('No calendar data to export')
        data = self.calendar.generateToICS(self.eventData['shift'])
        print('ics generated')
        icsdata = filedialog.asksaveasfile(defaultextension="ics", title="ICS bestand voor uw kalender app")

    def closeApplication(self):
        self.destroy()
        exit()
