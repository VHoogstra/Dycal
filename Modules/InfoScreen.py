import os
import shutil
import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint
from tkinter import filedialog

import customtkinter as ctk

from Modules.Constants import Constants
from Modules.Logger import Logger


class InfoScreen(tk.Toplevel):
  def __init__(self):
    tk.Toplevel.__init__(self)
    window_width = 500
    window_height = 400

    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.title('Dyflexis Details')
    self.configure(background=Constants.zaantheaterColor)
    # self.resizable(False, False)
    frame = tk.Frame(self)
    frame.grid(column=0, row=0, sticky=tk.NSEW)
    frame.configure(background=Constants.zaantheaterColor)

    tk.Message(frame,
               text="Deze applicatie is geschreven door Vincent Hoogstra in eigen tijd, Dyflexis zal altijd leidend blijven en het is mogelijk dat er bugs in de software staan. Er word geadviseerd om het ICS bestand dan ook niet in je hoofd agenda te stoppen maar in een losse agenda\n\n vragen en bug meldingen kunnen naar me.vincentvandetechniek.nl\n\n het helpt enorm als je de data exporteert naar een folder en het log bestand van de dag van de error naar mij toe stuurt\n\n tips,features of suggesties? gooi het op de mail!",
               fg='white', bg=Constants.zaantheaterColor,
               justify=tk.LEFT,
               anchor=tk.W,
               aspect=500,
               width=400,
               relief=tk.SUNKEN,
               ).grid(column=0,row=0,columnspan=3,sticky=tk.NSEW,padx=10,pady=10)
    ctk.CTkButton(frame,text='Export Files',command=self.exportFiles).grid(column=1, row=1)

  def exportFiles(self):
    print(' export files')
    target_dir = filedialog.askdirectory(
      title="ICS bestand van uw kalender app",
      initialdir=os.path.expanduser('~/Downloads'))

    source_dir = Constants.resource_path(Logger.logPrefix)

    file_names = os.listdir(source_dir)

    for file_name in file_names:
      shutil.move(os.path.join(source_dir, file_name), target_dir)
  def up(self):
    self.lift()
