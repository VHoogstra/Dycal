import os
import tkinter
import tkinter.ttk as ttk
import tkinter as tk
from idlelib.tooltip import TooltipBase, Hovertip
from tkinter import filedialog, Message, messagebox
import traceback
from pprint import pprint

import customtkinter as ctk
import arrow
from Modules.Google import Google

from Modules.Constants import Constants
from Modules.ICS import ICS
from Modules.Logger import Logger


class ExportWidgetGoogle(tk.Frame):
  calendar = None
  questionResponse=None

  def __init__(self, parent=None, gui=None, **kwargs):
    tk.Frame.__init__(self, parent, **kwargs)
    self.gui = gui
    self.google = Google()

    iscInfoText = 'Deze google integratie zal na het drukken op \"sync Google\" inloggen bij google en alle evenemeten ' \
                  'in een eigen agenda wegschrijven.\n De naam van deze agenda kan hernoemt worden zonder problemen. de software ' \
                  'verwijderd automatisch agenda afpsraken uit deze agenda die niet in dyflexis staan\n link je google voor het eerst? ' \
                  'dan opent er een webbrowser waarin je toestemming kan geven aan deze app'
    icsInfo = tk.Message(self,
                         text=iscInfoText,
                         fg='white',
                         bg=Constants.zaantheaterColor,
                         relief=tk.SUNKEN, anchor=tk.W,
                         width=360)
    icsInfo.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=5)

    tk.Button(self, text='force login Google', command=self.forceLoginGoogle,cursor="hand2").grid(row=1, column=1, sticky=tk.NSEW)
    tk.Button(self, text='sync Google', command=self.syncGoogle,cursor="hand2").grid(row=3, column=0, sticky=tk.NSEW)

    oepsieButton = tk.Button(self, text='oepsie doepsie de agenda is foetsie', command=self.clearcalenderId,cursor="hand2")
    oepsieButton.grid(row=2, column=0, sticky=tk.NSEW)
    Hovertip(anchor_widget=oepsieButton, text='verwijder de huidige geregistreerde agenda voor als er afgemeld is ipv verwijderd', hover_delay=None)

    self.feedbackMessageVar= tk.StringVar()
    self.feedbackMessage = tk.Label(self,
                                    textvariable=self.feedbackMessageVar,
                         fg='white',
                         bg=Constants.zaantheaterColor,
                         relief=tk.SUNKEN, anchor=tk.W,justify="left"
                        )
    self.feedbackMessage.grid(row=4,column=0,columnspan=3,sticky=tk.NSEW)

  def clearcalenderId(self):
    response = messagebox.askyesnocancel("Agenda verwijderen", "Wilt u ook de agenda verwijderen uit google", parent=self)

    if response is None:
      return
    self.feedbackMessagebuilder('Agenda aan het verwijderen',blank=True)
    self.google.login()
    googleConfig = self.gui.config.getKey('google')

    if response:
      self.feedbackMessagebuilder('google Agenda verwijderd\n')
      if googleConfig['calendarId'] is not None:
        self.google.getCalendarService().remove(googleConfig['calendarId'])
    else:
      self.feedbackMessagebuilder('google Agenda niet aangeraakt maar ik weet niet meer waar hij is\n ik maak een nieuwe aan volgende keer')
    googleConfig['calendarId'] = None
    self.gui.config.storeKey('google', googleConfig)

  def forceLoginGoogle(self):
    self.google.forceLogin()

  def feedbackMessagebuilder(self,message, blank=False):
    if blank:
      self.feedbackMessageVar.set(message)
    else:
      self.feedbackMessageVar.set(self.feedbackMessageVar.get() + message)
    self.gui.update()

  def syncGoogle(self):
    self.feedbackMessagebuilder("start sync\n",blank=True)
    self.feedbackMessagebuilder("Gebruiker inloggen:")

    self.google.login()
    self.feedbackMessagebuilder("\tLogin goed\n"+"Agenda opvragen:")

    googleCal = self.google.manageCalendar()
    self.feedbackMessagebuilder("\tGoogle agenda goed opgehaald\n")

    print('got a calendar')
    msg = "Succesvol de agenda geupdate"
    try:

      if self.gui.eventData is not None and 'shift' in self.gui.eventData :
        self.google.manageEvents(googleCal, self.gui.eventData['shift'])
      else:
        msg = "Er is nog geen evenementen data om te synchroniseren"
      self.feedbackMessagebuilder(msg)
    except Exception as e:
      Logger.getLogger(__name__).error('Er ging iets mis tijdens synchroniseren', exc_info=True)
      self.feedbackMessagebuilder("\ter ging wat mis\n")
      self.feedbackMessagebuilder(e)

    print('end of syncgoogle')

    # self.feedbackMessage.configure(text=msg)

