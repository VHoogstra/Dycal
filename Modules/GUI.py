import json
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import traceback
import arrow
from pprint import pprint

import customtkinter as ctk

from Modules.ConfigLand import ConfigLand
from Modules.Constants import Constants
from Modules.Dyflexis import Dyflexis
from Modules.DyflexisDetails import DyflexisDetails
from Modules.InfoScreen import InfoScreen
from Modules.Logger import Logger
from Modules.ICS import ICS


class Gui(tk.Frame):
  driver = None
  calendar = None
  eventDate = {}
  dyflexisMessage = "test "
  infoScreen = None

  def __init__(self, master=None):
    tk.Frame.__init__(self, master)

    self.eventData = None
    self.periods = []
    self.dyflexisProgressBarValue = tk.IntVar()
    self.grid(column=0, row=0, sticky=tk.NSEW)

    self.master.title('Dyflexis -> ICS calendar '+Constants.version)

    # self.master.attributes("-topmost", True)

    w = 430  # width for the Tk root
    h = 630  # height for the Tk root

    ws = self.master.winfo_screenwidth()

    hs = self.master.winfo_screenheight()

    x = ws / 3
    y = (hs / 2) - (h / 2)

    self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # nee resize is niet toegestaan
    # self.master.resizable(False, False)
    self.createPeriods()
    self.createWidgets()
    self.config = ConfigLand()
    self.master.lift()
    index = 6
    for period in self.periods:
      grid = dict(column=0, row=index)
      self.createLoader(self.dyflexisFrame, 1, self.periods[period], grid)
      index += 1

  def closingInfoScreen(self):
    self.infoScreen.destroy()
    self.infoScreen = None

  def openInfoScreen(self):
    if self.infoScreen == None:
      self.infoScreen = InfoScreen()
      self.infoScreen.protocol("WM_DELETE_WINDOW", self.closingInfoScreen)
    else:
      self.infoScreen.up()
  def createWidgets(self):
    self.mainFrame = ctk.CTkScrollableFrame(self, width=410, height=620)
    self.mainFrame.grid(column=0, row=0, sticky=tk.NSEW)
    self.mainFrame.configure(fg_color=Constants.zaantheaterColor)

    self.mainFrame.columnconfigure([0, 1, 2], weight=1)
    self.mainFrame.rowconfigure(1, minsize=10)

    self.configLoad = ctk.CTkButton(self.mainFrame, text='info', command=self.openInfoScreen)
    self.configLoad.grid(row=0, column=2, sticky=tk.N + tk.E, padx=5, pady=5)



    self.segmentedButtonSave = ctk.CTkSegmentedButton(self.mainFrame, values=["laad uit config", "save naar config"],
                                                         command=self.segmented_button_callback)
    self.segmentedButtonSave.grid(row=0, column=0,columnspan=2, sticky=tk.N + tk.W, padx=5, pady=5)
    # row 3
    label = tk.Label(text='Dyflexis', fg="white", bg=Constants.zaantheaterColor, width=10, height=1, )
    self.dyflexisFrame = tk.LabelFrame(self.mainFrame, labelwidget=label, bg=Constants.zaantheaterColor, padx=10,
                                       pady=10)
    self.dyflexisFrame.grid(row=3, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)
    self.dyflexisFrame.columnconfigure(0, weight=1)
    self.dyflexisFrame.columnconfigure([1, 2], weight=4)

    self.createLabel(text="username", parent=self.dyflexisFrame).grid(row=1, column=0)
    self.dyflexisUsername = self.createEntry(parent=self.dyflexisFrame)
    self.dyflexisUsername.grid(row=1, column=1, columnspan=2, sticky=tk.NSEW)

    self.createLabel(text="Password", parent=self.dyflexisFrame).grid(row=2, column=0)
    self.dyflexisPassword = self.createEntry(parent=self.dyflexisFrame)
    self.dyflexisPassword.grid(row=2, column=1, columnspan=2, sticky=tk.NSEW)

    ctk.CTkButton(
      self.dyflexisFrame,
      text='Dyflexis uitlezen',
      command=self.dyflexisRead
    ).grid(
      row=4,
      column=1,
      columnspan=1,
      pady=15
    )
    self.dyflexisMessage = tk.Message(self.dyflexisFrame,
                                      text="Nog geen informatie",
                                      fg='white', bg=Constants.zaantheaterColor,
                                      justify=tk.LEFT,
                                      anchor=tk.W,
                                      aspect=500,
                                      width=400,
                                      relief=tk.SUNKEN,

                                      )
    self.dyflexisMessage.grid(row=14, column=0, columnspan=2, sticky=tk.NSEW, pady=5)
    ctk.CTkButton(self.dyflexisFrame,
                  text='details',
                  command=self.openDyflexisDetails,
                  width=50
                  ).grid(row=14,
                         column=2,
                         sticky=tk.E,
                         pady=10
                         )

    GoogleLabel = tk.Label(text='ICS configuratie',
                           fg="white",
                           bg=Constants.zaantheaterColor,
                           width=15,
                           height=1, )
    IcsConfigurationFrame = tk.LabelFrame(self.mainFrame,
                                          labelwidget=GoogleLabel,
                                          bg=Constants.zaantheaterColor,
                                          padx=10,
                                          pady=10)
    IcsConfigurationFrame.grid(row=8,
                               column=0,
                               columnspan=3,
                               sticky=tk.NSEW,
                               padx=5, pady=5)
    IcsConfigurationFrame.columnconfigure([0, 2], weight=1)
    IcsConfigurationFrame.columnconfigure([1], weight=5)

    iscInfoText = "Een ICS bestand kan gegenereerd worden zonder een bestaand bestand te openen, echter als je twee keer dezelfde maand draait zal je dubbele afspraken krijgen.\nOmdat dit onpraktisch is kan je een link naar een openbare ics file toevoegen OF een geëxporteerd bestand uploaden. \nWij zullen in de afspraken zoeken naar dyflexis evenementen (door het ID in de omschrijving) en deze updaten"
    icsInfo = tk.Message(IcsConfigurationFrame,
                         text=iscInfoText,
                         fg='white',
                         bg=Constants.zaantheaterColor,
                         relief=tk.SUNKEN, anchor=tk.W,
                         width=360)
    icsInfo.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=5)

    self.createLabel(text="ics url",
                     parent=IcsConfigurationFrame).grid(row=1, column=0, sticky=tk.NSEW)
    self.icsUrl = self.createEntry(parent=IcsConfigurationFrame)
    self.icsUrl.grid(row=1, column=1, columnspan=1, sticky=tk.NSEW, padx=10)
    ctk.CTkButton(IcsConfigurationFrame, text='Laad ICS uit URL',
                  command=self.loadICS).grid(row=1, column=2, columnspan=1, padx=10, pady=2)

    ctk.CTkButton(IcsConfigurationFrame,
                  text='Open ICS bestand',
                  command=self.uploadICS).grid(row=2,
                                               column=0,
                                               columnspan=3,
                                               pady=10,
                                               sticky=tk.NSEW)
    ctk.CTkButton(IcsConfigurationFrame,
                  text='Genereer ICS',
                  command=self.generateICS).grid(row=3, column=0, columnspan=3, pady=10, sticky=tk.NSEW)

    self.ICSMessage = tk.Message(IcsConfigurationFrame,
                                 text='nog geen informatie',
                                 fg='white', bg=Constants.zaantheaterColor,
                                 anchor=tk.W,
                                 justify=tk.LEFT,
                                 relief=tk.SUNKEN,
                                 width=360)
    self.ICSMessage.grid(row=5,
                         column=0,
                         columnspan=4,
                         sticky=tk.NSEW)

  def segmented_button_callback(self,selection):
    #reset buttons so you can press one again
    self.segmentedButtonSave.set(value=4)
    if selection == "laad uit config":
      self.loadConfig()
    if selection=="save naar config":
      self.saveConfig()


  def createLabel(self, text, parent=None, **kwargs):
    if parent == None:
      parent = self
    return ctk.CTkLabel(
      parent,
      **kwargs,
      text=text,
      width=10,
      height=1, text_color='white'
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

  def updateDyflexisProgressBar(self, amount, period):
    if not isinstance(amount, tk.IntVar):
      temp = tk.IntVar()
      temp.set(amount)
      amount = temp

    print('updateDyflexisProgressbar -' + period + ": " + str(amount.get()))
    self.periods[period]["progress"].set(amount.get())
    # self.dyflexisProgressBarValue.set(value=amount.get())
    self.periods[period]['progressbar'].update()

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
                             self.master.winfo_screenheight())
    periodsToRun = []
    for period in self.periods:
      if (self.periods[period]['on'].get()):
        periodsToRun.append(period)
        self.updateDyflexisProgressBar(0,period)
    pprint(periodsToRun)
    self.lift()
    try:
      self.eventData = self.dyflexis.run(
        _progressbarCallback=self.updateDyflexisProgressBar,
        periods=periodsToRun
      )
    except Exception as e:
      Message = ('Er ging iets mis bij dyflexis: ')
      Logger().log(str(type(e)))
      if hasattr(e, 'message'):
        Message = Message + e.message
        Logger().log((e.message))
      else:
        Message = Message + str(e)
      Logger().log((traceback.format_exc()))

      self.dyflexisMessage.config(text=Message, bg='red', fg='white')
      raise e

    # with open('logs/latestCalendarData.json', 'r') as fp:
    #     superValue = fp.read()
    #     self.eventData = json.loads(superValue)
    #     fp.close()

    # create the information message for the GUI
    assignments = str(self.eventData['assignments'])
    agenda = str(self.eventData['agenda'])
    events = str(self.eventData['events'])
    start_date = self.eventData['list'][0]['date']
    end_date = self.eventData['list'][len(self.eventData['list']) - 1]['date']
    #todo check het verschil tussen windows en apple hier.. op windows gaat het goed maar op apple hebben we een extra whitespace?
    Message = f"Shifts: \t{assignments} \nAgenda: \t{agenda} \nEvents: \t{events} \nperiode: \t{start_date} tot {end_date}"
    pprint(Message)
    self.dyflexisMessage.config(text=Message, bg='green')

  def uploadICS(self):
    if self.calendar is None:
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
    if self.calendar is None:
      self.calendar = ICS()
    if self.icsUrl.get() is not None:
      self.calendar.connectToICS(url=self.icsUrl.get())
    print('loadIcs')
    ##todo give feedback

  def generateICS(self):
    print('generateICS')
    if self.calendar is None:
      self.calendar = ICS()
      # raise Exception('No calendar data to export')
    print('ics generated')
    name = "Dyflexis-ICS- " + arrow.now().format('YYYY-MM-DD')
    icsdata = filedialog.asksaveasfile(
      defaultextension="ics",
      title="ICS bestand voor uw kalender app",
      initialfile=name)
    if icsdata is None:  # asksaveasfile return `None` if dialog closed with "cancel".
      return
      # todo throw error?
    try:
      data = self.calendar.generateToICS(self.eventData['shift'])
    except Exception as e:
      Message = ('Er ging iets mis bij het genereren van ICS: ')
      Logger().log(str(type(e)))
      if hasattr(e, 'message'):
        Message = Message + e.message
        Logger().log((e.message))
      else:
        Message = Message + str(e)
      Logger().log((traceback.format_exc()))

      self.ICSMessage.config(text=Message, bg='red', fg='white')
      raise e

    icsdata.writelines(data)
    icsdata.close()

  def closeApplication(self):
    self.destroy()
    exit()

  def openDyflexisDetails(self):
    print('openDyflexisDetails')

    # with open('logs/latestCalendarData.json', 'r') as fp:
    #   superValue = fp.read()
    #   self.eventData = json.loads(superValue)
    #   fp.close()
    dyflexisDetails = DyflexisDetails(self.eventData)

  def createPeriods(self):
    self.periods = dict()
    for x in range(0, 4):
      onValue = tk.BooleanVar()
      if arrow.now().shift(months=2) > arrow.now().shift(months=x):
        onValue.set(True)
      self.periods.update({
        arrow.now().shift(months=x).format('YYYY-MM'): dict(
          period=arrow.now().shift(months=x).format('YYYY-MM'),
          on=onValue,
          progress=tk.IntVar()
        )
      })

  def createLoader(self, parent, variable, period, grid):

    grid.update(padx=0, pady=3)
    checkbar = ctk.CTkCheckBox(parent,
                               text=period['period'],
                               onvalue=True,
                               offvalue=False,
                               variable=period['on'],
                               text_color="white")
    checkbar.grid(column=grid['column'], row=grid['row'])

    grid.update(columnspan=2, sticky=tk.NSEW, column=grid['column'] + 1)
    progressBar = ttk.Progressbar(parent, mode='determinate', maximum=101,
                                  variable=period['progress'])
    progressBar.grid(grid)
    period.update(progressbar=progressBar)
