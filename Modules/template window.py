import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint

import customtkinter as ctk

from Modules.Constants import Constants


class template(tk.Toplevel):
  def __init__(self, eventData):
    tk.Toplevel.__init__(self)
    window_width = 500
    window_height = 400
    self.eventData = eventData

    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    # self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.title('Dyflexis Details')
    self.master.configure(background=Constants.primary_color)
    # self.resizable(False, False)
    frame = tk.Frame(self)
    frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    frame.configure(background=Constants.primary_color)