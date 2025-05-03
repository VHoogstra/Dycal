import time
import tkinter as tk
from tkinter import ttk

import arrow
import customtkinter as ctk

from Modules.Constants import Constants
from Modules.Google import Google
from Modules.Logger import Logger
from Modules.dataClasses import ExportReturnObject


class ScreenDataProcess(tk.Toplevel):
  def __init__(self, exportData: ExportReturnObject, continueButton,feedbackMessageBuilder = None):
    tk.Toplevel.__init__(self)
    window_width = 500
    window_height = 400
    self.exportData = exportData
    self.continueButton = continueButton
    self.feedbackMessageBuilder = feedbackMessageBuilder

    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.title('Dyflexis Export Data')
    self.master.configure(background=Constants.primary_color)
    # self.resizable(False, False)

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    if self.continueButton:
      ctk.CTkButton(self,text='Data is correct, doorvoeren',command=self.uploadToGoogle).grid(row=1, column=0, sticky=tk.NSEW,padx=10,pady=10)

    tabview = ctk.CTkTabview(master=self, width=525)
    tabview.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
    tabs = ["Nieuwe data: " + str(len(self.exportData.newCalendarItem)),
            "Agenda te updaten: " + str(len(self.exportData.updateCalendarItem)),
            "te verwijderen data: " + str(len(self.exportData.removeCalendarItem))]
    data = [self.exportData.newCalendarItem,self.exportData.updateCalendarItem,self.exportData.removeCalendarItem]
    for index,tab in enumerate(tabs):
      tabview.add(tab)
      tabview.tab(tab).columnconfigure(0, weight=1)
      tabview.tab(tab).rowconfigure(0, weight=1)

      columns = ('Datum', 'Naam')
      treeview = ttk.Treeview(
        master=tabview.tab(tab),
        columns=columns,
        show='headings')
      for column in columns:
        treeview.heading(column, text=column)
      treeview.grid(row=0, column=0, sticky=tk.NSEW)
      if data[index] is not None and len(data[index]) != 0:
        for item in data[index]:
          ##dit is een google item removal
          if 'etag' in item and 'dycolDate' not in item:
            item['dycolDate'] = arrow.get(item['start']['dateTime'],tzinfo=Constants.timeZone).format('YYYY-MM-DD HH:mm')
            item['dycolName'] = item['summary']
          if 'dycolDate' in item:
            item['dycolDate']= arrow.get(item['dycolDate'],tzinfo=Constants.timeZone).format('YYYY-MM-DD HH:mm')
          treeview.insert("", tk.END, values=(item['dycolDate'],item['dycolName']))

  def uploadToGoogle(self):
    self.loader = ctk.CTkProgressBar(self, mode='determinate', width=50)
    self.loader.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10)
    self.loader.set(value=0)
    try:
      googleObject = Google.getGoogleObject()
      googleObject.processData(googleObject.retrieveGoogleCalendar(),self.exportData,loaderUpdate=self.updateLoader)
      time.sleep(5)
    except Exception as e:
      Logger.getLogger(__name__).error('Er ging iets mis tijdens uploaden google', exc_info=True)
      if self.feedbackMessageBuilder is not None:
        self.feedbackMessageBuilder("\ter ging wat met de upload\n")
        message = Constants.Exception_to_message(e)
        self.feedbackMessageBuilder(message)
    if self.feedbackMessageBuilder is not None:
      self.feedbackMessageBuilder('\ngeupload naar google')
    self.destroy()

  def updateLoader(self,amount):
    self.loader.set(amount)
    self.loader.update()

