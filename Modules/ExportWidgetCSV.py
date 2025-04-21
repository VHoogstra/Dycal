import tkinter as tk
from tkinter import filedialog

import arrow
import customtkinter as ctk

from Modules.Constants import Constants
from Modules.Csv import Csv
from Modules.Logger import Logger


class ExportWidgetCSV(tk.Frame):
  calendar = None

  def __init__(self, parent=None, gui=None, **kwargs):
    tk.Frame.__init__(self, parent, **kwargs)
    self.gui = gui
    self.configure(bg=Constants.background_color_primary)

    iscInfoText = "Deze module genereerd een ; gescheiden CSV bestand.\nDe use case voor deze module is voornamelijk exporteren van de data"
    "mocht u een andere use case hebben en meer data of andere data willen exporteren, neem gerust contact op"
    icsInfo = tk.Message(self,
                         text=iscInfoText,
                         fg='white',
                         bg=Constants.zaantheaterColor,
                         relief=tk.SUNKEN, anchor=tk.W,
                         width=360)
    icsInfo.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=5)
    ctk.CTkButton(self, text='ParseData', command=self.parseData).grid(row=1, column=0, sticky=tk.NSEW, pady=5, padx=10)
    ctk.CTkButton(self, text='export', command=self.storeData).grid(row=1, column=2, sticky=tk.NSEW, pady=5, padx=10)

    self.feedback = ctk.CTkLabel(self, text="", anchor=tk.W, width=360, padx=10)
    self.feedback.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW, pady=5)

    self.update()
    self.feedback.configure(wraplength=self.feedback.winfo_width() - 35)

  def parseData(self):
    try:
      self.returnData = Csv().parseData(self.gui.eventData)
      self.feedback.configure(fg_color=Constants.zaantheaterColor, text_color='white', text="klaar met parsen van data",
                              padx=5, pady=5)

    except Exception as e:
      Message = Constants.Exception_to_message(e)
      Logger.getLogger(__name__).error('parseData error', exc_info=True)
      self.feedback.configure(fg_color='red', text_color='white', text=Message)


  def storeData(self):
    name = "Dycal-csv-" + arrow.get().format('YYYY-MM-DD')
    try:
      csvLocation = filedialog.asksaveasfilename(defaultextension="csv", title="csv bestand voor u", initialfile=name)
      if csvLocation is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
      Csv().exportToCsv(location=csvLocation, returnObject=self.returnData)
      self.feedback.configure(fg_color=Constants.zaantheaterColor, text_color='white',
                              text='klaar met het genereren van de csv', padx=5, pady=5)

    except Exception as e:
      Message = Constants.Exception_to_message(e)
      Logger.getLogger(__name__).error('parseData error', exc_info=True)
      self.feedback.configure(fg_color='red', text_color='white', text=Message)
