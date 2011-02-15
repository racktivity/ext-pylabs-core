from twisted.application.service import Application
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.plugins.applicationserver_plugin import serviceMaker
from twisted.python.logfile import DailyLogFile, BaseLogFile

import os
import time
from pylabs import q

class ApplicationserverLogFile(DailyLogFile):
    '''
    rotate log file daily or if size is greater than 100M
    '''
    def __init__(self, name, directory):
        self.originalName = name
        self.name = "%s.%s" % (self.originalName, self.suffix(self.toDate()))
        BaseLogFile.__init__(self, self.originalName, directory)

    def toDate(self, *args):
        return  time.localtime(*args)[:5]

    def shouldRotate(self):
        return self.toDate()[:3] > self.lastDate[:3] or self._file.tell() >= 100000000

    def rotate(self):
        if not (os.access(self.directory, os.W_OK) and os.access(self.path, os.W_OK)):
            return
        newpath = "%s.%s" % (q.system.fs.joinPaths(q.system.fs.getDirName(self.path), self.originalName), self.suffix(self.lastDate))
        if os.path.exists(newpath):
            return

        self._file.close()
        q.system.fs.moveFile(self.path, newpath)
        self._openFile()

application = Application("applicationserver")

ser = serviceMaker.makeService({'config':'applicationserver'})
ser.setServiceParent(application)
logfile = ApplicationserverLogFile("applicationserver.log", q.dirs.logDir)
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
