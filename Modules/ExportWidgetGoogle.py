import os
import tkinter.ttk as ttk
import tkinter as tk
import traceback
from pprint import pprint
from tkinter import filedialog

import customtkinter as ctk
import arrow
from Modules.Google import Google

from Modules.Constants import Constants
from Modules.ICS import ICS
from Modules.Logger import Logger


class ExportWidgetGoogle(tk.Frame):
  calendar = None
  def __init__(self, parent=None,gui=None, **kwargs):
    tk.Frame.__init__(self, parent, **kwargs)
    self.gui = gui
    self.google = Google()

    iscInfoText =" er word nog gewerkt aan deze integratie - "+str(self.google.validCreds())
    icsInfo = tk.Message(self,
                         text=iscInfoText,
                         fg='white',
                         bg=Constants.zaantheaterColor,
                         relief=tk.SUNKEN, anchor=tk.W,
                         width=360)
    icsInfo.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=5)

    tk.Button(self,text='force login Google',command=self.forceLoginGoogle).grid(row=1, column=1, sticky=tk.NSEW)
    tk.Button(self,text='sync Google',command=self.syncGoogle).grid(row=3, column=0, sticky=tk.NSEW)
    tk.Button(self,text='oepsie doepsie de agenda is foetsie',command=self.clearcalenderId).grid(row=2, column=0, sticky=tk.NSEW)
    # flow is auth login
    # check of er is ingelogd? kan ik dat displayen?
    # uitlezen en updaten
    #moet ook nog het id setten van de agenda
  def clearcalenderId(self):
    #todo set calid config to null
    googleConfig = self.gui.config.getKey('google')
    googleConfig['calendarId'] = None
    self.gui.config.storeKey('google', googleConfig)

  def forceLoginGoogle(self):
    self.google.forceLogin()

  def syncGoogle(self):
    self.google.login()
    print('google login succesvol ')
    googleCal= self.google.manageCalendar()
    pprint(googleCal)
    print(' got a calendar')
    # self.google.manageEvents(googleCal,self.gui.eventData['shift'])