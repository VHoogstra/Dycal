import json
import os
import queue
import sys
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import traceback
import arrow
from configparser import ConfigParser
from pprint import pprint

import customtkinter as ctk

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
        self.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        self.master.title('Dyflexis -> ICS calendar')
        self.master.configure(background=self.zaantheaterColor)

        w = 410  # width for the Tk root
        h = 600  # height for the Tk root

        ws = self.master.winfo_screenwidth()

        hs = self.master.winfo_screenheight()

        x = ws / 3
        if x < self.minChromeWidth:
            x = self.minChromeWidth
        y = (hs / 2) - (h / 2)
        x = 10

        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # nee resize is niet toegestaan
        self.master.resizable(False, False)
        self.createWidgets()
        self.config = ConfigLand()

        self.master.lift()

    def createWidgets(self):
        self.configure(background=self.zaantheaterColor)
        self.columnconfigure([0, 1, 2], weight=1, minsize=100)
        self.rowconfigure(1, minsize=20)
        # 4, tussen dyflexis config en resultaat
        self.rowconfigure(4, minsize=15)
        # tussen dyflexis en ics
        self.rowconfigure(6, minsize=20)
        self.master.rowconfigure(7, minsize=20)

        self.configLoad = ctk.CTkButton(self, text='Laad uit config', command=self.loadConfig)
        self.configLoad.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.save = ctk.CTkButton(self, text='save naar config', command=self.saveConfig)
        self.save.grid(row=0, column=2, sticky=tk.N + tk.E)

        # row 3
        label = tk.Label(text='Dyflexis', fg="white", bg=self.zaantheaterColor, width=10, height=1, )
        dyflexisFrame = tk.LabelFrame(self, labelwidget=label, bg=self.zaantheaterColor, padx=10, pady=10)
        dyflexisFrame.grid(row=3, column=0, columnspan=3, sticky=tk.NSEW)
        dyflexisFrame.rowconfigure(3, minsize=10)
        dyflexisFrame.columnconfigure(0, weight=1)
        dyflexisFrame.columnconfigure([1, 2], weight=4)

        self.createLabel(text="username", parent=dyflexisFrame).grid(row=1, column=0)
        self.dyflexisUsername = self.createEntry(parent=dyflexisFrame)
        self.dyflexisUsername.grid(row=1, column=1, columnspan=2, sticky=tk.NSEW)

        self.createLabel(text="Password", parent=dyflexisFrame).grid(row=2, column=0)
        self.dyflexisPassword = self.createEntry(parent=dyflexisFrame)
        self.dyflexisPassword.grid(row=2, column=1, columnspan=2, sticky=tk.NSEW)

        ctk.CTkButton(dyflexisFrame, text='Dyflexis uitlezen', command=self.dyflexisRead).grid(row=4, column=1,
                                                                                               columnspan=1)

        dyflexisLabel = tk.Label(text='Dyflexis resultaat', fg="white", bg=self.zaantheaterColor, width=15, height=1, )
        dyflexisResultaatFrame = tk.LabelFrame(self, labelwidget=dyflexisLabel, bg=self.zaantheaterColor, padx=10,
                                               pady=10)
        dyflexisResultaatFrame.columnconfigure(0, weight=1)
        dyflexisResultaatFrame.grid(row=5, column=0, columnspan=3, sticky=tk.W + tk.N + tk.E + tk.S)

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
        IcsConfigurationFrame = tk.LabelFrame(self, labelwidget=GoogleLabel, bg=self.zaantheaterColor, padx=10,
                                              pady=10)
        IcsConfigurationFrame.grid(row=8, column=0, columnspan=3, sticky=tk.W + tk.N + tk.E + tk.S)
        IcsConfigurationFrame.columnconfigure([0, 1], weight=1)
        IcsConfigurationFrame.columnconfigure([2], weight=3)

        self.createLabel(text="ics url",
                         parent=IcsConfigurationFrame).grid(row=1, column=0, sticky=tk.NSEW)
        self.icsUrl = self.createEntry(parent=IcsConfigurationFrame)
        self.icsUrl.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=10)

        # self.createLabel(text="of",
        #                  parent=IcsConfigurationFrame,
        #                  anchor='center').grid(row=0, column=0,columnspan=3,sticky=tk.NSEW)

        ctk.CTkButton(IcsConfigurationFrame,
                      text='Open ICS bestand',
                      command=self.uploadICS).grid(row=2, column=2, sticky=tk.NS + tk.E)

        ctk.CTkButton(IcsConfigurationFrame, text='Laad ICS uit URL',
                      command=self.loadICS).grid(row=1, column=1, columnspan=1, padx=10, pady=2)

        tk.Message(IcsConfigurationFrame,
                   text='nog geen informatie',
                   fg='white', bg='red',
                   justify=tk.LEFT).grid(row=5,
                                         column=0,
                                         columnspan=4,
                                         sticky=tk.N + tk.S + tk.W + tk.E)
        ctk.CTkButton(IcsConfigurationFrame,
                      text='Genereer ICS',

                      command=self.generateICS).grid(row=4, column=1, columnspan=5, pady=10)

    def createLabel(self, text, parent=None, **kwargs):
        if parent == None:
            parent = self
        return ctk.CTkLabel(
            parent,
            **kwargs,
            text=text,
            width=10,
            height=1,
        )

    def createEntry(self, parent=None, variable=None, **kwargs):
        if parent == None:
            parent = self
        return ctk.CTkEntry(
            parent,
            **kwargs,
            width=50,
            textvariable=variable
        )

    def loadConfig(self):
        print(' load goncig')
        self.config.loadConfig()
        self.dyflexisPassword.delete(0, 500)
        self.dyflexisPassword.insert(0, self.config.Config['dyflexis']['password'])

        self.dyflexisUsername.delete(0, 500)
        self.dyflexisUsername.insert(0, self.config.Config['dyflexis']['username'])

        self.icsUrl.delete(0, 500)
        self.icsUrl.insert(0, self.config.Config['ics']['url'])
    def setConfig(self):
        self.config.Config['dyflexis']['username'] = self.dyflexisUsername.get()
        self.config.Config['dyflexis']['password'] = self.dyflexisPassword.get()

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

    def validateEntry(self, entry):
        if entry.get() == "":
            entry.configure(fg_color='red')
            return False
        entry.configure(fg_color=['#F9F9FA', '#343638'])
        return True

    def dyflexisRead(self):
        error = False
        if not self.validateEntry(self.dyflexisPassword):
            error = True
        if not self.validateEntry(self.dyflexisUsername):
            error = True
        if error:
            return
        self.setConfig()

        self.dyflexis = Dyflexis(self.config,
                                 self.master.winfo_screenwidth(),
                                 self.master.winfo_screenheight(),
                                 self.minChromeWidth)
        try:
            self.eventData = self.dyflexis.run(_progressbarCallback=self.updateDyflexisProgressBar)
        except Exception as e:
            Message = ('Er ging iets mis bij dyflexis: ')
            Logger().log(str(type(e)))
            if hasattr(e,'message'):
                Message = Message + e.message
                Logger().log((e.message))
            else:
                Message = Message + str(e)
            Logger().log((traceback.format_exc()))


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
        icsdata = filedialog.askopenfilename(
            filetypes=[('ICS bestand', 'ics')],
            title="ICS bestand van uw kalender app",
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
        print('ics generated')
        name = "Dyflexis->ICS- "+arrow.now().format('YYYY-MM-DD')
        icsdata = filedialog.asksaveasfile(
            defaultextension="ics",
            title="ICS bestand voor uw kalender app",
        initialfile=name)
        if icsdata is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
            #todo throw error?
        data = self.calendar.generateToICS(self.eventData['shift'])
        icsdata.writelines(data)
        icsdata.close()

    def closeApplication(self):
        self.destroy()
        exit()