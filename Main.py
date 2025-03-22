#!/usr/bin/env python

from Modules.ConfigLand import ConfigLand
from Modules.GUI import Gui
from Modules.Logger import Logger
from Modules.Dyflexis import Dyflexis

######## function land ########

def closeApplication():
    print("waiting, press enter to cclose")
    # driver.quit()
#https://tkdocs.com/shipman/index-2.html

######## Main #########
useConfigFile = True
global config
config = ConfigLand(useConfigFile)


app = Gui()
app.mainloop()

# todo, mogelijkheid om ook via firefox of safari te draaien?
# driver = webdriver.Chrome()

#todo hier moet het ww dus al ingevuld zijn in config?

# check of we kunnen inloggen

### dyflexis =  Dyflexis(driver,config)
# if dyflexis.login() != True:
#     closeApplication()
#
#
# closeApplication()
#
#
#
# #calendarArray =tableToArray(calendar)
# print(calendarArray)
# writeToFile(calendarArray)

closeApplication()
    
    






