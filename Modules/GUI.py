import json
import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint

import arrow

import customtkinter as ctk

from Modules.ConfigLand import ConfigLand
from Modules.Constants import Constants
from Modules.Dyflexis import Dyflexis
from Modules.DyflexisDetails import DyflexisDetails
from Modules.ExportWidget import ExportWidget
from Modules.InfoScreen import InfoScreen
from Modules.Logger import Logger
from Modules.dataClasses import PeriodList, EventDataList
from Modules.debug import DebugWindow
from Modules.periodGui import PeriodGui


class Gui(tk.Frame):
  driver = None
  eventDate = {}
  dyflexisMessage = "test "
  infoScreen = None
  debugWindow = None
  configLand: ConfigLand = None

  def openDebug(self, element):
    if self.debugWindow is None:
      self.debugWindow = DebugWindow(self)
    else:
      self.debugWindow.destroy()
      self.debugWindow = None

  def testKey(self, element, event):
    print(event.char, event.keysym, event.keycode)
    pprint(element)

  def destroy(self):
    Logger.getLogger(__name__).info('closing application')
    if self.configLand is not None:
      self.configLand.save()
    super().destroy()

  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    ## key bindings
    self.master.bind("<Shift_L><D>", self.openDebug)
    self.master.bind("<Shift_R><D>", self.openDebug)
    # self.master.bind("<Key>", self.testKey)
    Logger.getLogger(__name__).info('starting Gui')

    self.eventData = None
    self.periods = PeriodList(3)
    self.periods.addHandler(self.updatePeriodLoaders)
    self.dyflexisProgressBarValue = tk.IntVar()
    self.grid(column=0, row=0, sticky=tk.NSEW)
    self.master.rowconfigure(0,weight=1)
    self.master.columnconfigure(0,weight=1)
    self.master.title('{}: {}'.format(Constants.appname, Constants.version))

    # self.master.attributes("-topmost", True)
    w = 860  # width for the Tk root
    h = 500  # height for the Tk root
    self.scrolWindowHeight = h - 10
    ws = self.master.winfo_screenwidth()
    hs = self.master.winfo_screenheight()

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # nee resize is niet toegestaan
    # self.master.resizable(False, False)
    self.configLand = ConfigLand()
    self.createWidgets()
    self.loadConfig()

    self.updatePeriodLoaders()

    self.configLand.addLoadHandler(self.loadConfig)
    self.configLand.addUpdateHandler(self.updateDyflexis)

    self.master.lift()

    self.placeExportWidget()
    Logger.getLogger(__name__).info('Gui initialized')

    self.update()
    self.dyflexisMessage.config(wraplength=self.dyflexisFrame.winfo_width() - 35)

    # self.openDebug('key')

  def closingInfoScreen(self):
    self.infoScreen.destroy()
    self.infoScreen = None

  def openInfoScreen(self):
    if self.infoScreen is None:
      self.infoScreen = InfoScreen()
      self.infoScreen.protocol("WM_DELETE_WINDOW", self.closingInfoScreen)
    else:
      self.infoScreen.up()

  def createWidgets(self):
    #todo hier moet een event listener op voor als we resizen
    self.mainFrame = ctk.CTkScrollableFrame(self, width=840, height=self.scrolWindowHeight)
    self.mainFrame.grid(column=0, row=0, sticky=tk.NSEW)
    self.mainFrame.configure(fg_color=Constants.zaantheaterColor)

    self.mainFrame.columnconfigure([0, 1, 2], weight=1)
    self.mainFrame.rowconfigure(1, minsize=10)

    self.configLoad = ctk.CTkButton(self.mainFrame, text='info', command=self.openInfoScreen)
    self.configLoad.grid(row=0, column=5, sticky=tk.N + tk.E, padx=5, pady=5)

    self.segmentedButtonSave = ctk.CTkSegmentedButton(self.mainFrame, values=[
      "reset config",
      'export config', 'import config'],
                                                      command=self.segmented_button_callback)
    self.segmentedButtonSave.grid(row=0, column=0, columnspan=5, sticky=tk.N + tk.W, padx=5, pady=5)
    # row 3
    label = tk.Label(text='Dyflexis', fg="white", bg=Constants.zaantheaterColor, width=10, height=1, )
    self.dyflexisFrame = tk.LabelFrame(self.mainFrame, labelwidget=label, bg=Constants.zaantheaterColor, padx=10,
                                       pady=10)
    self.dyflexisFrame.grid(row=3, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)
    self.dyflexisFrame.columnconfigure(0, weight=1)
    self.dyflexisFrame.columnconfigure([1, 2], weight=4)

    self.createLabel(text="Gebruikersnaam", parent=self.dyflexisFrame).grid(row=1, column=0)
    self.dyflexisUsername = self.createEntry(parent=self.dyflexisFrame, validatecommand=self.updateDyflexis)
    self.dyflexisUsername.grid(row=1, column=1, columnspan=2, sticky=tk.NSEW)
    self.dyflexisUsername.bind("<KeyPress>", self.updateDyflexis)

    self.createLabel(text="Wachtwoord", parent=self.dyflexisFrame).grid(row=2, column=0)
    self.dyflexisPassword = self.createEntry(parent=self.dyflexisFrame)
    self.dyflexisPassword.bind("<KeyPress>", self.updateDyflexis)
    self.dyflexisPassword.grid(row=2, column=1, columnspan=2, sticky=tk.NSEW)

    self.createLabel(text="Organisatie", parent=self.dyflexisFrame).grid(row=3, column=0)
    self.dyflexisOrganisatie = self.createEntry(parent=self.dyflexisFrame)
    self.dyflexisOrganisatie.bind("<KeyPress>", self.updateDyflexis)
    self.dyflexisOrganisatie.grid(row=3, column=1, columnspan=2, sticky=tk.NSEW)

    self.createLabel(text="Locatie", parent=self.dyflexisFrame).grid(row=4, column=0)
    self.dyflexisLocatie = self.createEntry(parent=self.dyflexisFrame)
    self.dyflexisLocatie.bind("<KeyPress>", self.updateDyflexis)
    self.dyflexisLocatie.grid(row=4, column=1, columnspan=2, sticky=tk.NSEW)

    ctk.CTkButton(
      self.dyflexisFrame,
      text='custom periodes..',
      command=self.openPeriodsGui
    ).grid(row=5, column=0, columnspan=1, pady=15)
    ctk.CTkButton(
      self.dyflexisFrame,
      text='Dyflexis uitlezen',
      command=self.dyflexisRead
    ).grid(row=5, column=1, columnspan=1, pady=15)
    self.dyflexisProgressFrame = tk.Frame(self.dyflexisFrame)
    self.dyflexisProgressFrame.grid(row=6, column=0, columnspan=3, sticky=tk.NSEW)
    self.dyflexisProgressFrame.columnconfigure(0, weight=0)
    self.dyflexisProgressFrame.columnconfigure(1, weight=1)
    self.dyflexisProgressFrame.configure(bg=Constants.zaantheaterColor)
    self.dyflexisMessageVariable = tk.StringVar()
    self.dyflexisMessageVariable.set('Nog geen informatie bekend')
    self.dyflexisMessage = tk.Label(self.dyflexisFrame,
                                    textvariable=self.dyflexisMessageVariable,
                                    fg='white', bg=Constants.zaantheaterColor,
                                    justify=tk.LEFT,
                                    anchor=tk.W,
                                    relief=tk.SUNKEN,
                                    wraplength=330, padx=5, pady=5
                                    )
    self.dyflexisFrame.columnconfigure(2, weight=0, minsize=10)
    self.dyflexisFrame.rowconfigure(14, weight=1, minsize=10)
    self.dyflexisMessage.grid(row=15, column=0, columnspan=3, sticky=tk.NSEW, pady=5)
    ctk.CTkButton(self.dyflexisFrame,
                  text='details',
                  command=self.openDyflexisDetails,
                  width=50
                  ).grid(row=14, column=2, sticky=tk.E, pady=10)

  def segmented_button_callback(self, selection):
    # reset buttons so you can press one again
    self.segmentedButtonSave.set(value=4)
    if selection == "reset config":
      self.resetConfig()
    if selection == 'export config':
      self.configLand.exportConfig()
    if selection == 'import config':
      self.configLand.importConfig()
      self.loadConfig()

  def openPeriodsGui(self):
    PeriodGui(self.periods)

  def createLabel(self, text, parent=None, **kwargs):
    if parent == None:
      parent = self
    return ctk.CTkLabel(
      parent,
      text=text,
      width=10,
      height=1, text_color='white',
      **kwargs,
    )

  def placeExportWidget(self):
    Logger.getLogger(__name__).info('opening export window')
    self.exportWidget = ExportWidget(self.mainFrame, gui=self)
    self.exportWidget.grid(row=3,
                           column=3,
                           columnspan=3,
                           sticky=tk.NSEW, )

  def createEntry(self, parent=None, variable=None, **kwargs):
    if parent == None:
      parent = self
    return ctk.CTkEntry(
      parent,
      **kwargs,
      width=50,
      textvariable=variable
    )

  def updateDyflexis(self, *args):
    dyflexis_data = self.configLand.getKey('dyflexis')
    dyflexis_data['username'] = self.dyflexisUsername.get()
    dyflexis_data['password'] = self.dyflexisPassword.get()
    dyflexis_data['organisation'] = self.dyflexisOrganisatie.get()
    dyflexis_data['location'] = self.dyflexisLocatie.get()
    self.configLand.setKey('dyflexis', dyflexis_data)

  def loadConfig(self):
    Logger.getLogger(__name__).info('loading config')
    dyflexisConfig = self.configLand.getKey('dyflexis')
    self.dyflexisPassword.delete(0, 500)
    self.dyflexisPassword.insert(0, dyflexisConfig['password'])

    self.dyflexisUsername.delete(0, 500)
    self.dyflexisUsername.insert(0, dyflexisConfig['username'])

    self.dyflexisOrganisatie.delete(0, 500)
    self.dyflexisOrganisatie.insert(0, dyflexisConfig['organisation'])

    self.dyflexisLocatie.delete(0, 500)
    self.dyflexisLocatie.insert(0, dyflexisConfig['location'])

  def resetConfig(self):
    Logger.getLogger(__name__).info('reseting config')
    self.configLand.reset()



  def validateEntry(self, entry):
    if entry.get() == "":
      entry.configure(fg_color='red')
      return False
    entry.configure(fg_color=['#F9F9FA', '#343638'])
    return True

  def dyflexisRead(self):
    error = False
    if not self.validateEntry(self.dyflexisPassword):
      Logger.getLogger(__name__).warning('Wachtwoord is leeg')
      error = True
    if not self.validateEntry(self.dyflexisUsername):
      Logger.getLogger(__name__).warning('Gebruikersnaam is leeg')
      error = True
    if not self.validateEntry(self.dyflexisOrganisatie):
      Logger.getLogger(__name__).warning('Organisatie is leeg')
      error = True
    if not self.validateEntry(self.dyflexisLocatie):
      Logger.getLogger(__name__).warning('Locatie is leeg')
      error = True

    if error:
      return
    self.configLand.handleUpdateHandlers()

    self.dyflexis = Dyflexis(self.configLand,
                             self.master.winfo_screenwidth(),
                             self.master.winfo_screenheight())


    # reset the periods to 0 in progressbar
    periodsToRun = []
    for period in self.periods.getPeriods():
      if period.on :
        periodsToRun.append(period)
        period.updateProgressBar(0)
    Logger.getLogger(__name__).info('periodes die gerunt gaan worden: %a ', ' , '.join(str(x.period) for x in periodsToRun))
    self.lift()
    self.update()
    try:
      self.eventData = self.dyflexis.run(
        periods=periodsToRun,
      )
      if self.configLand.getKey('persistentStorageAllowed') == True:
        Logger.toFile(location=Constants.logPrefix + Constants.dyflexisJsonFilename, variable=self.eventData.toJson(),
                      isJson=True)

      # self.loadFromBackup()
    except Exception as e:
      Message = ('Er ging iets mis bij dyflexis:\n')
      if hasattr(e, 'message'):
        Message = Message + e.message
      else:
        Message = Message + str(e)
      Logger.getLogger(__name__).error('Er ging wat mis bij bij dyflexis.run', exc_info=True)
      self.dyflexisMessage.config(bg='red', fg='white')
      self.dyflexisMessageVariable.set(Message)
      return

    # create the information message for the GUI
    Message = self.printDyflexisEventDataMessage()
    Logger.getLogger(__name__).info('dyflexis run klaar met bericht %a', Message)
    self.dyflexisMessage.config(bg='green')
    self.dyflexisMessageVariable.set(Message)

  def printDyflexisEventDataMessage(self):
    # create the information message for the GUI
    assignments = str(self.eventData.assignments)
    agenda = str(self.eventData.agenda)
    events = str(self.eventData.events)
    if len(self.eventData.list) == 0:
      start_date = "null"
      end_date = "null"
    else:
      start_date = self.eventData.list[0]['date']
      end_date = self.eventData.list[len(self.eventData.list) - 1]['date']
    return "Shifts: {}\nAgenda: {}\nEvents: {}\nperiode: {} tot {}".format(assignments, agenda, events, start_date,
                                                                              end_date)
  def closeApplication(self):
    self.destroy()
    exit()

  def openDyflexisDetails(self):
    Logger.getLogger(__name__).info('open Dyflexis Details')
    dyflexisDetails = DyflexisDetails(self.eventData)

  def updatePeriodLoaders(self):
    # redraw periods and remove unused periods
    for widget in self.dyflexisProgressFrame.winfo_children():
      widget.destroy()
    row = 0
    for period in self.periods.getPeriods():
      self.createLoader(self.dyflexisProgressFrame, period, {'row': row, 'column': 0})
      row += 1

  def createLoader(self, parent, period, grid):
    grid.update(padx=3, pady=3)
    checkbar = ctk.CTkCheckBox(parent,
                               text=period.period,
                               onvalue=True,
                               offvalue=False,
                               variable=period.getTkOn(),
                               command=period.checkboxCallback,
                               text_color="white")
    checkbar.grid(column=grid['column'], row=grid['row'], pady=grid['pady'])

    grid.update(columnspan=2, sticky=tk.NSEW, column=grid['column'] + 1)
    progressBar = ttk.Progressbar(parent, mode='determinate', maximum=101,
                                  variable=period.getTkProgress())
    progressBar.grid(grid)
    period.progressBar = progressBar
    period._checkbox = checkbar

  def loadFromBackup(self):
    Logger.getLogger(__name__).info('load from backup')
    with open('logs/latestCalendarData.json', 'r+') as fp:
      superValue = fp.read()
      self.eventData = EventDataList()
      data = json.loads(superValue)
      self.eventData.assignments = data['assignments']
      self.eventData.agenda = data['agenda']
      self.eventData.events = data['events']
      self.eventData.periods = data['periods']
      self.eventData.list = data['list']
      self.eventData.shift = data['shift']
      fp.close()
    Message = self.printDyflexisEventDataMessage()
    self.dyflexisMessage.config(bg='green')
    self.dyflexisMessageVariable.set(Message)
