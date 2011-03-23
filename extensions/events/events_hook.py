from pylabs import q
from rabbitmqclient import Connection
from events import EXCHG_NAME, EXCHG_TYPE
from events.event_consumer_mgr import EventConsumerMgr

class Events(object):
    
    def __init__(self):
        self._con = Connection()
    
    def publish(self, rootingKey, tagString):
        self._con.publish(EXCHG_NAME, rootingKey, tagString)

    def _getConsumerPath(self, appName):
        return q.system.fs.joinPaths(q.dirs.pyAppsDir, appName, 'impl', 'events')

    def startConsumers(self, appName):
        EventConsumerMgr(self._getConsumerPath(appName)).start()
    
    def stopConsumers(self, appName):
        EventConsumerMgr(self._getConsumerPath(appName)).stop()
