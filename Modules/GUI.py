import json
import tkinter as tk

from selenium import webdriver

from Modules.ConfigLand import ConfigLand
from Modules.Dyflexis import Dyflexis
from Modules.Logger import Logger
from Modules.ICS import ICS
from selenium.webdriver.chrome.options import Options


class Gui(tk.Frame):
    zaantheaterColor = "#7a4689"
    driver = None
    eventDate = {}
    dyflexisMessage = "test "
    minChromeWidth = 1027

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W, padx=10, pady=10)
        self.config = ConfigLand()
        self.createWidgets()

        self.master.title('Dyflexis -> Google calendar')
        self.master.configure(background=self.zaantheaterColor)
        self.master.lift()

        w = 430  # width for the Tk root
        h = 600  # height for the Tk root

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        x = ws / 3
        if x < self.minChromeWidth:
            x = self.minChromeWidth
        y = (hs / 2) - (h / 2)

        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master.columnconfigure(0, minsize=40)
        ##new line na boven en onder dyflexys

        # nee resize is niet toegestaan
        self.master.resizable(False, False)

    def createWidgets(self):
        self.configure(background=self.zaantheaterColor)
        self.rowconfigure(2, minsize=40)
        self.rowconfigure(4, minsize=20)
        self.rowconfigure(7, minsize=20)
        self.columnconfigure(7, minsize=300)
        self.columnconfigure(6, minsize=40)

        self.quit = tk.Button(self, text='Laad uit config', command=self.loadConfig, fg='white', bg='black')
        self.quit.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W)
        self.save = tk.Button(self, text='save naar config', command=self.saveConfig, fg='white', bg='black')
        self.save.grid(row=0, column=3, sticky=tk.N + tk.S + tk.W)

        googleLabel = tk.Label(text='Dyflexis', fg="white", bg=self.zaantheaterColor, width=10, height=1, )
        dyflexisFrame = tk.LabelFrame(self, labelwidget=googleLabel, bg=self.zaantheaterColor, padx=10, pady=10)
        dyflexisFrame.grid(row=3, column=0, columnspan=6, sticky=tk.W + tk.N)
        self.createLabel(text="username", anchor=dyflexisFrame).grid(row=1, column=1)
        self.dyflexisUsername = self.createEntry(anchor=dyflexisFrame)
        self.dyflexisUsername.grid(row=1, column=2)

        self.createLabel(text="Password", anchor=dyflexisFrame).grid(row=2, column=1)
        self.dyflexisPassword = self.createEntry(anchor=dyflexisFrame)
        self.dyflexisPassword.grid(row=2, column=2)

        tk.Button(self, text='Dyflexis uitlezen', fg='white', bg='black', command=self.dyflexisRead).grid(row=5,
                                                                                                          column=0)
        dyflexisLabel = tk.Label(text='Dyflexis resultaat', fg="white", bg=self.zaantheaterColor, width=15, height=1, )
        dyflexisResultaatFrame = tk.LabelFrame(self, labelwidget=dyflexisLabel, bg=self.zaantheaterColor, padx=10,
                                               pady=10)
        dyflexisResultaatFrame.columnconfigure(0, weight=1)
        dyflexisResultaatFrame.grid(row=6, column=0, columnspan=6, sticky=tk.W + tk.N + tk.E + tk.S)

        self.dyflexisMessage = tk.Message(dyflexisResultaatFrame, text="Nog geen informatie", fg='white', bg='red',
                                          justify=tk.LEFT,
                                          aspect=500,
                                          width=300)
        self.dyflexisMessage.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        GoogleLabel = tk.Label(text='ics configuratie', fg="white", bg=self.zaantheaterColor, width=15, height=1, )
        googleResultaatFrame = tk.LabelFrame(self, labelwidget=GoogleLabel, bg=self.zaantheaterColor, padx=10,
                                             pady=10)
        googleResultaatFrame.grid(row=8, column=0, columnspan=6, sticky=tk.W + tk.N + tk.E + tk.S)
        googleResultaatFrame.columnconfigure(0, weight=1)
        self.createLabel(text="ics url", anchor=googleResultaatFrame).grid(row=1, column=0)
        self.icsUrl = self.createEntry(anchor=googleResultaatFrame)
        self.icsUrl.grid(row=1, column=1)
        self.createLabel(text="of ", anchor=googleResultaatFrame).grid(row=2, column=0)
        self.createLabel(text="of bestand", anchor=googleResultaatFrame).grid(row=3, column=0)
        self.iscFile = self.createEntry(anchor=googleResultaatFrame)
        self.iscFile.grid(row=3, column=1)
        tk.Message(googleResultaatFrame, text='nog geen informatie', fg='white', bg='red', justify=tk.LEFT).grid(row=4,
                                                                                                                 column=0,
                                                                                                                 columnspan=2,
                                                                                                                 sticky=tk.N + tk.S + tk.W + tk.E)
        tk.Button(self, text='Laad ICS', fg='white', bg='black', command=self.loadICS).grid(row=9, column=0)
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

    def openChrome(self):
        if self.driver == None:
            ws = self.master.winfo_screenwidth() / 3
            if ws < self.minChromeWidth:
                ws = self.minChromeWidth
            hs = self.master.winfo_screenheight()
            print('window-size=%d,%d' % (ws, hs))
            options = Options()
            # options.add_argument("--headless")
            options.add_argument('window-size=%d,%d' % (ws, hs))
            self.driver = webdriver.Chrome(options=options)

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

    def dyflexisRead(self):
        # open json file
        ## todo ,wat als er nog geen inlog gegevens zijn ingevuld, validatie dus

        self.openChrome()
        dyflexis = Dyflexis(self.driver, self.config)
        dyflexis.login()
        calendar = dyflexis.getRooster()
        calendarData = dyflexis.tableElementToArray(calendar)
        logger = Logger()
        logger.toFile(location='calendarData.json', variable=calendarData)
        self.eventData = dyflexis.elementArrayToIcs(calendarData)
        self.driver.quit()
        self.driver = None
        logger.toFile(location='icsData.json', variable=self.eventData)

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
        print('uploadIcs')

    def loadICS(self):
        self.calendar = ICS()
        if (self.icsUrl.get() != None):
            self.calendar.connectToICS(url=self.icsUrl.get())
        print('loadIcs')
        # upload een bestaand of pak het uit een folder
        # merge met lijst van dyflexis aan de hand
        # exporteerd de lijst naar een bestand

    def generateICS(self):
        print('generateICS')
        self.calendar.generateToICS(self.eventData['shift'])
        print('ics generated')
        # todo, alleen evenementen van vandaag en vooruit oppakken. in het verleden niet
