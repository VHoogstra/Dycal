import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint
import customtkinter as ctk

from Modules.Constants import Constants
from Modules.ExportWidgetCSV import ExportWidgetCSV
from Modules.ExportWidgetGoogle import ExportWidgetGoogle
from Modules.ExportWidgetICS import ExportWidgetICS


class ExportWidget(ctk.CTkTabview):
  def __init__(self, parent,gui=None):
    ctk.CTkTabview.__init__(self,parent)
    self.gui = gui
    window_width = 500
    window_height = 400
    self.parent = parent

    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    # self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    # self.resizable(False, False)
    self.add("ICS")  # add tab at the end
    self.add("CSV")  # add tab at the end
    self.add("Google")  # add tab at the end
    # tabview.set("agenda items")  # set currently visible tab
    self.set("Google")  # set currently visible tab

    # grid(self.tab("agenda items"))
    self.exportWidgetICS = ExportWidgetICS(parent=self.tab('ICS'), gui=self.gui)
    self.exportWidgetICS.grid(row=0, column=0, sticky=tk.NSEW,padx=5,pady=5)

    self.exportWidgetCSV = ExportWidgetCSV(parent=self.tab('CSV'), gui=self.gui)
    self.exportWidgetCSV.grid(row=0, column=0, sticky=tk.NSEW,padx=5,pady=5)

    self.exportWidgetGoogle = ExportWidgetGoogle(parent=self.tab('Google'), gui=self.gui)
    self.exportWidgetGoogle.grid(row=0, column=0, sticky=tk.NSEW,padx=5,pady=5)

