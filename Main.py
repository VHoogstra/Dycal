#!/usr/bin/env python3
import sys

from Modules.ConfigLand import ConfigLand
from Modules.GUI import Gui
from Modules.Logger import Logger
from Modules.Dyflexis import Dyflexis

#https://tkdocs.com/shipman/index-2.html
######## Main #########

app = Gui()
app.mainloop()
print('mainloop ended')
sys.exit(0)

