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

# dyflexis = Dyflexis({},3,3)
# events=[
#         {
#           "id": "event://1725",
#           "text": "Kz ISH Dance Collective - Home",
#           "description": ""
#         },
#         {
#           "id": "event://1726",
#           "text": "AH Simon Keizer - Ruimte",
#           "description": "Status: Bevestigd\n\n14:30: Aankomst techniek\n20:00: Aanvang\n21:30: Einde\n\nAantal techniek: 3\nAantal verkochte tickets: 214"
#         },
#         {
#           "id": "event://1724",
#           "text": "ZTR Diner in ZaanTheaterrestaurant",
#           "description": ""
#         }
#       ]
# assignments={
#           "id": "assignment://21094",
#           "tijd": "13:00 - 23:00",
#           "text": "Zaandam > 60 Technische Dienst > Grote zaal"
#         }
# for event in events:
#     print(dyflexis.eventNameParser(event,assignments))
# test = input(' test')

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

