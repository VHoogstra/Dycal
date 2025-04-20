import tkinter as tk

from Modules.Constants import Constants


class ScreenException(tk.Frame):
  def __init__(self, message,exception):
    tk.Frame.__init__(self)
    window_width = 500
    window_height = 400
    self.message = message
    self.exception = exception

    # get screen dimension
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # create the screen on window console
    self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # self.attributes("-topmost", True)
    self.master.title('dyclol exception')
    self.master.configure(background=Constants.zaantheaterColor)
    # self.resizable(False, False)
    self.master.columnconfigure(0, weight=1)
    self.master.rowconfigure(0, weight=1)
    label = tk.Label(self.master,text=self.message)
    label.grid(column=0, row=0,sticky=tk.NSEW)
    self.master.update()
    label.config(wraplength=label.winfo_width() - 35)

