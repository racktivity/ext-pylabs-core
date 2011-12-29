from pylabs import q
from events import EXCHG_NAME
from events.event_consumer_mgr import EventConsumerMgr

class Events(object):

    def __init__(self):
        self._connections = dict()

    def getConnection(self, host):
        from events.rabbitmqclient import Connection
        if host not in self._connections:
            self._connections[host] = Connection(host)
        return self._connections[host]
    
    def publish(self, rootingKey, tagString, host='127.0.0.1'):
        self.getConnection(host).publish(EXCHG_NAME, rootingKey, tagString)

    def _getConsumerPath(self, appName):
        appDir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appName)
        if not q.system.fs.isDir(appDir):
            raise RuntimeError("No pyapp with name '%s' found" % appName)
        return q.system.fs.joinPaths(appDir, 'impl', 'events')

    def startConsumers(self, appName):
        path = self._getConsumerPath(appName)
        if q.system.fs.exists(path):
            EventConsumerMgr(appName, path).start()
    
    def stopConsumers(self, appName):
        path = self._getConsumerPath(appName)
        if q.system.fs.exists(path):
            EventConsumerMgr(appName, path).stop()
