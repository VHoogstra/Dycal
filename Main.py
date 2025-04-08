#!/usr/bin/env python3
import sys
import traceback

from Modules.Constants import Constants
from Modules.GUI import Gui
from Modules.Google import Google
from Modules.Logger import Logger


#https://tkdocs.com/shipman/index-2.html
######## Main #########

Constants.cleanLogFolder()
# print(sys.argv)
# for arg in sys.argv:
#     if "--headless" in arg:
#         print("Headless mode")

try:
    app = Gui()
    app.mainloop()

except Exception as e:
    Message = ('Er ging iets mis in de mainloop: ')
    Logger().log(str(type(e)))
    if hasattr(e, 'message'):
        Message = Message + e.message
        Logger().log((e.message))
    else:
        Message = Message + str(e)
    Logger().log((traceback.format_exc()))
    print(Message)
    raise e
    sys.exit(0)

print('mainloop ended')
sys.exit(0)

