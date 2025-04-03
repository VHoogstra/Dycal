#!/usr/bin/env python3
import os
import sys
import traceback

from Modules.ConfigLand import ConfigLand
from Modules.GUI import Gui
from Modules.Logger import Logger
from Modules.Dyflexis import Dyflexis
from dotenv import load_dotenv


#https://tkdocs.com/shipman/index-2.html
######## Main #########




load_dotenv()
# print(os.getenv('LOGIN_URL'))

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
    sys.exit(0)

print('mainloop ended')
sys.exit(0)

