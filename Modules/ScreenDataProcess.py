import tkinter as tk
from datetime import tzinfo
from tkinter import ttk

import arrow
import customtkinter as ctk

from Modules.Constants import Constants
from Modules.dataClasses import ExportReturnObject


class ScreenDataProcess(tk.Toplevel):
  def __init__(self, exportData: ExportReturnObject, google):
    tk.Toplevel.__init__(self)
    window_width = 500
    window_height = 400
    self.exportData = exportData
    self.google = google

    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    # self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.title('Dyflexis Export Data')
    self.master.configure(background=Constants.primary_color)
    # self.resizable(False, False)

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    tabview = ctk.CTkTabview(master=self, width=525)
    tabview.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
    tabs = ["Nieuwe data", "Agenda te updaten", "te verwijderen data"]
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
          treeview.insert("", tk.END, values=(item['dycolDate'],item['dycolName']))

