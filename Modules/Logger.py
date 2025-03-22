import json
import time

class Logger:
    def __init__(self):
        self.logPrefix = "./logs/log "

    def __str__(self):
        return 'i log important information'

    def log(self,msg):
        with open(self.logPrefix+time.strftime("%Y-%m-%d", time.gmtime())+'.txt', 'a') as fp:
            fp.write("\n")
            fp.write(time.strftime("%Y-%m-%d %H:%M", time.gmtime()))
            fp.write("\t")
            fp.write(msg)
            fp.close()
    def toFile(self,location,variable):
        with open(location,'w') as fp:
            fp.write(json.dumps(variable))
