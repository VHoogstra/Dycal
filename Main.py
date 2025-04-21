#!/usr/bin/env python3

from Modules.GUI import Gui
from Modules.Logger import Logger
from Modules.ScreenException import ScreenException
import customtkinter as ctk


def main():
    ######## Main #########
    Logger.getLogger(__name__).info(' ###\t\t\tapplication start\t\t\t###')

    try:
        ctk.set_appearance_mode("dark")
        app = Gui()
        app.mainloop()

    except Exception as e:
        Message = ('Er ging iets mis in de mainloop: ')
        if hasattr(e, 'message'):
            Message = Message + e.message
        else:
            Message = Message + str(e)
        Logger.getLogger(__name__).error('Er ging wat mis bij bij Mainloop', exc_info=True)
        #todo bug scherm openen?
        excep = ScreenException(Message, e)
        excep.mainloop()

if __name__ == "__main__":
    main()