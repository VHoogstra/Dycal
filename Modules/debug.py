import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint

import customtkinter as ctk
from customtkinter import CTkButton

from Modules.Constants import Constants


class DebugWindow(tk.Toplevel):


  def __init__(self,gui ):
    tk.Toplevel.__init__(self)
    window_width = 500
    window_height = 400
    self.gui = gui

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
    self.master.configure(background=Constants.zaantheaterColor)
    # self.resizable(False, False)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=0, minsize=100)

    self.messageVar = tk.StringVar()
    self.messageVar.set('leeg')
    self.message = tk.Message(self, textvariable=self.messageVar)
    self.message.grid(column=0, row=0)

    frame = tk.Frame(self)
    frame.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)

    self.debugItems = [
      {
        'type': 'labelframe',
        'txt': 'Dyflexis',
        'items': [
          {
            'type': 'checkbox',
            'txt': 'gebruik TestGenerator',
            'variable': None
          },
          {
            'type': 'button',
            'txt': 'load test data',
            'command': self.gui.loadFromBackup
          }
        ]
      },
      {
        'type': 'labelframe',
        'txt': 'Google',
        'items': [
          {
            'type': 'checkbox',
            'txt': 'gebruik TestGenerator',
            'variable': None
          },
        ]
      },
      {
        'type': 'labelframe',
        'txt': 'csv',
        'items': [
          {
            'type': 'checkbox',
            'txt': 'gebruik TestGenerator',
            'variable': None
          },
        ]
      },
    ]

    self.debugGenerator(frame, self.debugItems, 0, 1)

  def debugGenerator(self, master, items, rowCount, columnStart):
    for item in items:
      if item['type'] == 'checkbox':
        item['variable'] = tk.IntVar()
        self.createCheckBox(item, master, (rowCount, columnStart))
      if item['type'] == 'button':
        item['variable'] = tk.IntVar()
        self.createButton(item, master, (rowCount, columnStart))

      if item['type'] == 'labelframe':
        item['variable'] = tk.StringVar()
        labelFrame = self.createLabelFrame(item, master, (rowCount, columnStart))
        self.debugGenerator(labelFrame, item['items'], rowCount, columnStart)

      rowCount = rowCount + 1

  def createCheckBox(self, item, master, grid: (int, int)):
    """
    :param item: {txt,variable}
    :param master: frame to add to
    :param grid: row,column
    :return:
    """
    chkbtn = tk.Checkbutton(master, text=item['txt'])
    chkbtn.grid(column=grid[1], row=grid[0], sticky=tk.NSEW, padx=10, pady=10)
    return chkbtn

  def createLabelFrame(self, item, master, grid: (int, int)):
    labelframe = tk.LabelFrame(master, text=item['txt'])
    labelframe.grid(column=grid[1], row=grid[0], sticky=tk.NSEW, padx=10, pady=10)
    return labelframe

  def createButton(self,item,master,grid:(int, int)):
    button = CTkButton(master, text=item['txt'], command=item['command'])
    button.grid(column=grid[1], row=grid[0], sticky=tk.NSEW, padx=10, pady=10)
    return button