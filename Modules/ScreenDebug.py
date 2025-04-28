import tkinter as tk
from pprint import pprint
from venv import logger

from customtkinter import CTkButton

from Modules.Constants import Constants
from Modules.Logger import Logger, TailLogger
import customtkinter as ctk


class ScreenDebug(tk.Toplevel):


  def __init__(self,gui ):
    tk.Toplevel.__init__(self)
    Logger.getLogger(__name__).info("Initializing ScreenDebug")
    window_width = 800
    window_height = 400
    self.gui = gui
    self.configure(bg=Constants.background_color_primary)
    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.title('dycal debug')
    # self.resizable(False, False)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=0, minsize=100)

    self.messageVar = tk.StringVar()
    self.messageVar.set('')
    self.scrollbar = ctk.CTkScrollableFrame(self,width = int(window_width/2), height=window_height)
    self.scrollbar.grid(row=0, column=0, sticky='ns')
    self.message = ctk.CTkLabel(self.scrollbar,
                                textvariable=self.messageVar,
                                anchor=tk.N,bg_color='black',justify='left',
                                padx=5)
    self.message.grid(column=0, row=0,sticky=tk.NSEW)
    self.scrollbar.columnconfigure(0, weight=1)
    self.scrollbar.rowconfigure(0, weight=1)

    frame = tk.Frame(self)
    frame.grid(column=1, row=0, sticky=tk.NSEW, padx=10, pady=10)
    frame.configure(bg=Constants.background_color_primary)


    self.debugItems = [
      {
        'type': 'labelframe',
        'txt': 'Dyflexis',
        'items': [
          {
            'type': 'button',
            'txt': 'load test data',
            'command': self.gui.loadFromBackup
          },
          {
            'type': 'button',
            'txt': 'print log',
            'command': self.test
          }
        ]
      },
      {
        'type': 'labelframe',
        'txt': 'Google',
        'items': [
        ]
      },
      {
        'type': 'labelframe',
        'txt': 'csv',
        'items': [

        ]
      },
    ]
    self.update()
    self.message.configure(wraplength=self.message.winfo_width() - 40)
    self.writeConsole()
    TailLogger.addHandler(self.writeConsole)
    self.debugGenerator(frame, self.debugItems, 0, 1)
    self.bind("<Configure>", self._resize_grid)

  def _resize_grid(self, event):

    self.scrollbar.configure( width=event.width)


  def test(self):
    Logger.getLogger(__name__).info('test application')

  def writeConsole(self):
    test = Logger._tail.contents()
    self.messageVar.set(test)

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
    labelframe = tk.LabelFrame(master, text=item['txt'],fg='white',bg=Constants.background_color_primary)
    labelframe.grid(column=grid[1], row=grid[0], sticky=tk.NSEW, padx=10, pady=10)
    return labelframe

  def createButton(self,item,master,grid:(int, int)):
    button = CTkButton(master, text=item['txt'], command=item['command'])
    button.grid(column=grid[1], row=grid[0], sticky=tk.NSEW, padx=10, pady=10)
    return button