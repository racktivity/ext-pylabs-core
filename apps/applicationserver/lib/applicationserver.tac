import sys
import twisted.application.app
import twisted.internet.defer
import twisted.python.failure
orig_runReactorWithLogging = twisted.application.app.runReactorWithLogging

def patched_runReactorWithLogging(config, oldstdout, oldstderr, profiler=None, reactor=None):
    if not config['debug']:
        return orig_runReactorWithLogging(config, oldstdout, oldstderr, profiler, reactor)

    if reactor is None:
        from twisted.internet import reactor
    try:
        sys.stdout = oldstdout
        sys.stderr = oldstderr
        reactor.run()
    except:
        if config['nodaemon']:
            file = oldstdout
        else:
            file = open('TWISTD-CRASH.log', 'a')
        traceback.print_exc(file=file)
        file.flush()

twisted.application.app.runReactorWithLogging = patched_runReactorWithLogging

twisted.internet.defer.setDebugging(False)
twisted.python.failure.DO_POST_MORTEM = False

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

name = os.environ['TWISTED_NAME']
application = Application(name)

ser = serviceMaker.makeService({'config':name})
ser.setServiceParent(application)
logfile = ApplicationserverLogFile("%s.log" % name, q.dirs.logDir)
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
