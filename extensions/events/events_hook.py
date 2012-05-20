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

    def startConsumers(self, appName):
        EventConsumerMgr(appName).start()
    
    def stopConsumers(self, appName):
        EventConsumerMgr(appName).stop()

    def restartConsumers(self, appName):
        EventConsumerMgr(appName).restart()
