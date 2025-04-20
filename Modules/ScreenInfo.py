import os
import tkinter as tk
import webbrowser

import customtkinter as ctk

from Modules.Constants import Constants
from Modules.Logger import Logger


class ScreenInfo(tk.Toplevel):
  def __init__(self):
    tk.Toplevel.__init__(self)
    window_width = 500
    window_height = 400
    self.background_color_primary= '#393534'
    self.background_color_secondary= "#4a4747"
    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.title('dycal info')
    self.configure(background=self.background_color_primary)
    # self.resizable(False, False)
    frame = tk.Frame(self)
    frame.grid(column=0, row=0, sticky=tk.NSEW)
    frame.configure(background=self.background_color_primary)

    tk.Message(frame,
               text="Deze applicatie is geschreven door Vincent Hoogstra in eigen tijd, Dyflexis zal altijd leidend blijven en het is mogelijk dat er bugs in de software staan.\n\nVragen, ideeen, inspiratie en bug meldingen kunnen naar me.vincentvandetechniek.nl\n\nBij bugs/problemen helpt het als het log bestand mee gestuurd word en de json files samen met een omschrijving van wat er word verwacht en wat er gebeurt. In de .json bestanden staat je werk agenda in data weggezet\n\nTips, features of suggesties? gooi het op de mail!",
               fg='white', bg=self.background_color_secondary,
               justify=tk.LEFT,
               anchor=tk.W,
               aspect=500,
               width=400,
               relief=tk.SUNKEN,
               ).grid(column=0, row=0, columnspan=3, sticky=tk.NSEW, padx=10, pady=10)
    ctk.CTkButton(frame, text='Export Files', command=self.openFolder).grid(column=1, row=1)

    self.release = tk.Message(frame,
                              fg='white', bg=self.background_color_secondary,
                              justify=tk.LEFT,
                              anchor=tk.W,
                              aspect=500,
                              width=400,
                              relief=tk.SUNKEN,
                              )
    self.release.grid(column=0, row=2, columnspan=3, sticky=tk.NSEW, padx=10, pady=10)
    self.getVersion()

  def openFolder(self):
    Logger.getLogger(__name__).info(' open folder files')
    base_path = os.path.expanduser('~/' + Constants.userStorageLocation)
    path = os.path.realpath(base_path)
    webbrowser.open('file:///' + path)


  def getVersion(self):
    versie = Constants.githubVersion()
    text = f"De meest recente versie is {versie}\nDe huidige versie is {Constants.version}"
    self.release.config(text=text)
  def up(self):
    self.lift()
