import tkinter as tk

import arrow
import customtkinter as ctk

from Modules.Constants import Constants
from Modules.dataClasses import PeriodList, Period


class ScreenPeriod(tk.Toplevel):
  def __init__(self, periods: PeriodList):
    tk.Toplevel.__init__(self)
    window_width = 500
    window_height = 400
    self.periods = periods
    self.configure(bg=Constants.background_color_primary)

    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    # self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.title('custom periode')
    self.master.configure(background=Constants.zaantheaterColor)
    # self.resizable(False, False)
    # frame = tk.Frame(self)
    # frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    # frame.configure(background=Constants.zaantheaterColor)
    ctk.CTkLabel(self, text='van periode').grid(row=0, column=0, padx=5, pady=5)
    self.startPer = ctk.CTkEntry(self, placeholder_text="YYYY-MM")
    self.startPer.grid(row=1, column=0, padx=5, pady=5)
    ctk.CTkLabel(self, text='tot periode').grid(row=0, column=2, padx=5, pady=5)
    self.endPer = ctk.CTkEntry(self, placeholder_text="YYYY-MM")
    self.endPer.grid(row=1, column=2, padx=5, pady=5)

    self.feedback = ctk.CTkLabel(self, text="", padx=5, pady=5)
    self.feedback.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)

    ctk.CTkButton(self, text='genereer', command=self.generatePeriods).grid(row=3, column=0, columnspan=3, padx=5,
                                                                            pady=5)
    ctk.CTkButton(self, text='+ voor',
                  width=10,
                  corner_radius=20,
                  command=self.generatePeriodBeforeFirst).grid(row=4, column=0, padx=5,
                                                                            pady=5)
    ctk.CTkButton(self, text='+ na', width=10,
                  corner_radius=20, command=self.generatePeriodAfterLast).grid(row=4, column=2, padx=5,
                                                                            pady=5)
    self.frame = tk.Frame(self)
    self.frame.grid(row=5, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)
    self.frame.columnconfigure(0, weight=1)
    self.frame.columnconfigure(1, weight=0)

    self.periods.addHandler(self.updatePeriods)
    self.updatePeriods()
    self.update()
    self.feedback.configure(wraplength=self.feedback.winfo_width() - 35)


  def generatePeriodBeforeFirst(self):
    periods = self.periods.getPeriods()
    if len(periods) == 0:
      self.periods.addPeriod(Period())
    else:
      date = arrow.get(periods[0].period,tzinfo=Constants.timeZone).shift(months=-1).format('YYYY-MM')
      self.periods.addPeriod(Period(date))

  def generatePeriodAfterLast(self):
    periods = self.periods.getPeriods()
    if len(periods) == 0:
      self.periods.addPeriod(Period())
    else:
      date = arrow.get(periods[len(periods)-1].period,tzinfo=Constants.timeZone).shift(months=1).format('YYYY-MM')
      self.periods.addPeriod(Period(date))

  def updatePeriods(self):
    for widget in self.frame.winfo_children():
      widget.destroy()
    gridStart = 1
    for period in self.periods.getPeriods():
      gridStart = gridStart + 1
      ctk.CTkLabel(self.frame, text=period.period).grid(column=0, row=gridStart, padx=5, pady=5)
      ctk.CTkButton(self.frame, text='verwijderen', command=lambda var=period: self.removePeriod(var)).grid(column=1,
                                                                                                            row=gridStart,
                                                                                                            padx=5,
                                                                                                            pady=5)

  def removePeriod(self, period):
    self.periods.removePeriod(period)

  def generatePeriods(self):
    self.feedback.configure(fg_color='transparent', text_color="white", text='')
    try:
      self.periods.generatePeriods(self.startPer.get(), self.endPer.get())
    except Exception as e:
      Message = ('Er ging iets mis bij het genereren:\n')
      if hasattr(e, 'message'):
        Message = Message + e.message
      else:
        Message = Message + str(e)
      self.feedback.configure(fg_color='red', text_color="white", text=Message)
