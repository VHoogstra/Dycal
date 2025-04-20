import os
import tkinter.ttk as ttk
import tkinter as tk
import traceback
from tkinter import filedialog

import customtkinter as ctk
import arrow

from Modules.Constants import Constants
from Modules.Csv import Csv
from Modules.ICS import ICS
from Modules.Logger import Logger


class ExportWidgetCSV(tk.Frame):
  calendar = None
  def __init__(self, parent=None,gui=None, **kwargs):
    tk.Frame.__init__(self, parent, **kwargs)
    self.gui = gui
    iscInfoText =" er word nog gewerkt aan deze integratie"
    icsInfo = tk.Message(self,
                         text=iscInfoText,
                         fg='white',
                         bg=Constants.zaantheaterColor,
                         relief=tk.SUNKEN, anchor=tk.W,
                         width=360)
    icsInfo.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=5)
    ctk.CTkButton(self,text='ParseData',command=self.parseData).grid(row=1, column=0, sticky=tk.NSEW, pady=5)
    ctk.CTkButton(self,text='export',command=self.storeData).grid(row=2, column=0, sticky=tk.NSEW, pady=5)

  def parseData(self):
    self.returnData= Csv().parseData(self.gui.eventData)
  def storeData(self):
    name = "Dycal-csv- " + arrow.get().format('YYYY-MM-DD')

    csvLocation = filedialog.asksaveasfilename(
      defaultextension="csv",
      title="csv bestand voor u",
      initialfile=name)
    if csvLocation is None:  # asksaveasfile return `None` if dialog closed with "cancel".
      return
    Csv().exportToCsv(location=csvLocation,returnObject=self.returnData)