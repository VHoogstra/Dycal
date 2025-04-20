import os
import tkinter as tk
import traceback
from tkinter import filedialog

import arrow
import customtkinter as ctk

from Modules.ConfigLand import ConfigLand
from Modules.Constants import Constants
from Modules.ICS import ICS
from Modules.Logger import Logger


class ExportWidgetICS(tk.Frame):
  calendar = None
  #todo nog agenda items na lopen die niet aan een ass gelinkt zijn... die moeten dan verwijderd
  def __init__(self, parent=None,gui=None, **kwargs):
    tk.Frame.__init__(self, parent, **kwargs)
    self.gui = gui
    self.config = ConfigLand.getConfigLand()
    self.config.addUpdateHandler(self.updateConfig)
    self.config.addLoadHandler(self.loadFromConfig)


    iscInfoText = "Een ICS bestand kan gegenereerd worden zonder een bestaand bestand te openen, echter als je twee keer dezelfde maand draait zal je dubbele afspraken krijgen.\nOmdat dit onpraktisch is kan je een link naar een openbare ics file toevoegen OF een geëxporteerd bestand uploaden. \nWij zullen in de afspraken zoeken naar dyflexis evenementen (door het ID in de omschrijving) en deze updaten"
    icsInfo = tk.Message(self,
                         text=iscInfoText,
                         fg='white',
                         bg=Constants.zaantheaterColor,
                         relief=tk.SUNKEN, anchor=tk.W,
                         width=360)
    icsInfo.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=5)
    self.gui.createLabel(text="ics url",
                     parent=self).grid(row=1, column=0, sticky=tk.NSEW)
    self.icsUrl = self.gui.createEntry(parent=self)
    self.icsUrl.bind("<KeyPress>", self.updateConfig)
    self.icsUrl.grid(row=1, column=1, columnspan=1, sticky=tk.NSEW, padx=10)
    ctk.CTkButton(self, text='Laad ICS uit URL',
                  command=self.loadICS).grid(row=1, column=2, columnspan=1, padx=10, pady=2)

    ctk.CTkButton(self,
                  text='Open ICS bestand',
                  command=self.uploadICS).grid(row=2,
                                               column=0,
                                               columnspan=3,
                                               pady=10,
                                               sticky=tk.NSEW)
    ctk.CTkButton(self,
                  text='Genereer ICS',
                  command=self.generateICS).grid(row=3, column=0, columnspan=3, pady=10, sticky=tk.NSEW)

    self.ICSMessage = tk.Message(self,
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
    self.loadFromConfig()

  def updateConfig(self,*args):
    # window hasnt been visable yet
    if not hasattr(self,'icsUrl'):
      return
    Logger.getLogger(__name__).info('update config')
    icsConfig = self.config.getKey('ics')
    icsConfig['url'] = self.icsUrl.get()
    self.config.setKey('ics', icsConfig)

  def loadFromConfig(self):
    value = self.config.getKey('ics')['url']
    self.icsUrl.delete(0, 500)
    self.icsUrl.insert(0, value)

  def uploadICS(self):
    self.ICSMessage.config(bg=Constants.zaantheaterColor)
    if self.calendar is None:
      self.calendar = ICS()
    print('uploadIcs')
    icsdata = filedialog.askopenfilename(
      filetypes=[('ICS bestand', 'ics')],
      title="ICS bestand van uw kalender app",
      initialdir=os.path.expanduser('~/Downloads'))
    if icsdata is not None:
      try:
        self.calendar.connectToICS(file=icsdata)
      except Exception as e:
        Message = ('Er ging iets mis bij het openen van het ICS bestand: ')
        Logger().log(str(type(e)))
        if hasattr(e, 'message'):
          Message = Message + e.message
          Logger().log((e.message))
        else:
          Message = Message + str(e)
        Logger().log((traceback.format_exc()))
        self.ICSMessage.config(text=Message, bg='red', fg='white')
        raise e

    eventCount = len(self.calendar.calendar.events)
    self.ICSMessage.config(text=f"{eventCount} agenda items gevonden via bestand")

  def loadICS(self):
    self.ICSMessage.config(bg=Constants.zaantheaterColor)
    if self.calendar is None:
      self.calendar = ICS()
    if self.icsUrl.get() is not None:
      try:

        self.calendar.connectToICS(url=self.icsUrl.get())

      except Exception as e:
        Message = ('Er ging iets mis bij het openen van de ICS Link: ')
        Logger().log(str(type(e)))
        if hasattr(e, 'message'):
          Message = Message + e.message
          Logger().log((e.message))
        else:
          Message = Message + str(e)
        Logger().log((traceback.format_exc()))
        self.ICSMessage.config(text=Message, bg='red', fg='white')
        raise e
    print('loadIcs')
    eventCount = len(self.calendar.calendar.events)
    self.ICSMessage.config(text=f"{eventCount} agenda items gevonden via de link")

  def generateICS(self):
    self.ICSMessage.config(bg=Constants.zaantheaterColor)
    print('generateICS')
    if self.calendar is None:
      self.calendar = ICS()
    if self.gui.eventData == None:
      self.ICSMessage.config(
        text="Kan geen ICS bestand genereren als er geen evenementen data is, lees eerst Dyflexis uit.",
        bg='orange')
      return
      # raise Exception('No calendar data to export')
    print('ics generated')
    name = "Dycal-ICS- " + arrow.get().format('YYYY-MM-DD')
    icsdata = filedialog.asksaveasfile(
      defaultextension="ics",
      title="ICS bestand voor uw kalender app",
      initialfile=name)
    if icsdata is None:  # asksaveasfile return `None` if dialog closed with "cancel".
      return
    try:
      data = self.calendar.generateToICS(self.gui.eventData.shift)
    except Exception as e:
      Message = ('Er ging iets mis bij het genereren van ICS: ')
      Logger.getLogger(__name__).error('generateICS exception', exc_info=True)

      if hasattr(e, 'message'):
        Message = Message + e.message
      else:
        Message = Message + str(e)

      self.ICSMessage.config(text=Message, bg='red', fg='white')
      raise e

    icsdata.writelines(data)
    icsdata.close()