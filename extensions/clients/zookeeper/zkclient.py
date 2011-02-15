from pylabs import q
from pylabs.Shell import *

import zookeeper, time, datetime, threading

TIMEOUT = 10.0


ZOO_OPEN_ACL_UNSAFE = {"perms":0x1f, "scheme":"world", "id" :"anyone"}

class ZKClient(object):
    def __init__(self, servers,port=2181, timeout=TIMEOUT):
        """
        create connection to zookeeper
        @param server e.g. "localhost"
        @param port (std 2181)
        """
        self.connected = False
        self.conn_cv = threading.Condition( )
        self.handle = -1
        #@todo make cross platform
        zookeeper.set_log_stream(open("/dev/null"))   

        self.conn_cv.acquire()

        q.logger.log("Connecting to %s" % (servers))
        start = time.time()
        
        self.handle = zookeeper.init(servers, self._connection_watcher, 30000)
        self.conn_cv.wait(timeout)
        self.conn_cv.release()

        if not self.connected:
            raise RuntimeError("Unable to connect to %s" % (servers))

        q.logger.log("Connected in %d ms, handle is %d" % (int((time.time() - start) * 1000), self.handle))
                        

    def _connection_watcher(self, h, type, state, path):
        """
        checks the connection by watching the condition, if this function is called means connection was made
        """
        self.handle = h
        self.conn_cv.acquire()
        self.connected = True
        self.conn_cv.notifyAll()
        self.conn_cv.release()

    def close(self):
        return zookeeper.close(self.handle)    
    
    def create(self, path, data="", flags=0, acl=[ZOO_OPEN_ACL_UNSAFE]):
        start = time.time()
        if not self.exists(path):
            q.logger.log("Create item on zookeeper on path %s" % path)
            result = zookeeper.create(self.handle, path, data, acl, flags)
            print "create:"+result
        #q.logger.log("Node %s created in %d ms" % (path, int((time.time() - start) * 1000)))
        #return result

    def delete(self, path, version=-1):
        start = time.time()
        result = zookeeper.delete(self.handle, path, version)
        q.logger.log("Node %s deleted in %d ms" % (path, int((time.time() - start) * 1000)))
        return result

    def get(self, path, watcher=None):
        """
        (data,stat) = ....get(path)
        """
        return zookeeper.get(self.handle, path, watcher)

    def exists(self, path, watcher=None):
        return zookeeper.exists(self.handle, path, watcher)

    def set(self, path, data="", version=-1):
        return zookeeper.set(self.handle, path, data, version)

    def set2(self, path, data="", version=-1):
        return zookeeper.set2(self.handle, path, data, version)

    def getChildren(self, path, watcher=None):
        return zookeeper.get_children(self.handle, path, watcher)

    def async(self, path = "/"):
        return zookeeper.async(self.handle, path)

    def acreate(self, path, callback, data="", flags=0, acl=[ZOO_OPEN_ACL_UNSAFE]):
        result = zookeeper.acreate(self.handle, path, data, acl, flags, callback)
        return result

    def adelete(self, path, callback, version=-1):
        return zookeeper.adelete(self.handle, path, version, callback)

    def aget(self, path, callback, watcher=None):
        return zookeeper.aget(self.handle, path, watcher, callback)

    def aset(self, path, callback, data="", version=-1):
        return zookeeper.aset(self.handle, path, data, version, callback)

    def exchangeGet(self,exchangename):
        """
        get an exchange on which queues can be created
        """
        return ZooKeeperExchange(self,exchangename)
    
class ZooKeeperExchange(object):
    
    def __init__(self,zkconnection,exchangename):
        self.queues={}
        self.zkconnection=zkconnection
        self.name=exchangename
        self.zkconnection.create("/exchanges")        
        if self.zkconnection.exists("/exchanges/%s" % exchangename):
            children=self.zkconnection.getChildren("/exchanges/%s" % exchangename)
            for queuename in children:
                self.queues[queuename]=ZooKeeperQueue(self.zkconnection,self.name,queuename)        
        else:
            self.zkconnection.create("/exchanges/%s" % exchangename)
        
    def _queueGet(self,queuename):
        """
        return a queue attached to the exchange
        """
        if not self.queues.has_key(queuename):
            raise RuntimeError("queue %s not found in exchange %s" % (self.name,queuename))
        return self.queues[queuename]
        
    def queueCreate(self,queuename):
        """
        create a queue and attach to the exchange
        every message published to the exchange will be put on all queues of that exchange        
        """
        self.queues[queuename]=ZooKeeperQueue(self.zkconnection,self.name,queuename)
        
    def publish(self,message):
        """
        publish a message onto the exchange, all attached queues will receive the message
        """
        for key in self.queues.iterkeys():
            #q.logger.log("Publish message %s on queue %s" % (message,key),5)
            queue=self.queues[key]
            queue.publish(message)
            #print queue.get()
    
    def queueDelete(self,queueName):
        queue=self._queueGet(queueName)
        queue.delete()
        
    def queueGetMessage(self,queueName):
        queue=self._queueGet(queueName)
        queue.get()                
    
class ZooKeeperQueue(object):
    def __init__(self,zkconnection,exchangename,queuename):
        """
        @param zkconnection=active zookeeperconnection
        """
        self._zkconnection=zkconnection
        self.queuename = queuename
        self.exchangename=exchangename
        if not self._zkconnection.exists(self._getlocation()):
            self._zkconnection.create(self._getlocation(),"queue top level",0, [ZOO_OPEN_ACL_UNSAFE])
    
    def _getlocation(self,path=""):
        return "/exchanges/%s/%s%s" % (self.exchangename,self.queuename,path)
            
    def publish(self,message):
        self._zkconnection.create(self._getlocation("/item"), message, zookeeper.SEQUENCE,[ZOO_OPEN_ACL_UNSAFE])
    
        #@todo introduce enumerators for e.g. zookeeper.SEQUENCE
        
    def get(self,leaveOnQueue=False):
        """
        get item from queue but leave the item there
        """
        #while True:
        children = sorted(self._zkconnection.getChildren(self._getlocation("")))
        if len(children) == 0:
            return None
        for child in children:
            data = self._get(self._getlocation() + "/" + children[0],not leaveOnQueue)
            if data:
                return data
                
    def getall(self):
        result=[]
        data=self.get()
        while data:
            result.append(data)
            data=self.get()
        return result
    
    def empty(self):
        self.getall()
        
    def delete():
        #@todo
        pass
        
    def _get(self,path,delete=True):
        #try:
        (data,stat) = self._zkconnection.get(path)
        self._zkconnection.delete(path, stat["version"])
        return data
        #except IOError, e:
        #    if e.message == zookeeper.zerror(zookeeper.NONODE):
        #        return None 
        #    raise e
               
    ##def getWait(self):
        ##def queue_watcher(handle,event,state,path):
            ##self.cv.acquire()
            ##self.cv.notify()
            ##self.cv.release()            
        ##while True:    
            ##self.cv.acquire()
            ##children = sorted(zookeeper.get_children(self.handle, self.queuename, queue_watcher))
            ##for child in children:
                ##data = self.get_and_delete(self.queuename+"/"+children[0])
                ##if data != None:
                    ##self.cv.release()
                    ##return data            
            ##self.cv.wait()
            ##self.cv.release()
                  
    
class ZKClientFactory():
    
    def __init__(self):
        self.watchers={}
        
    def getConnection(self,servers, timeout=TIMEOUT):
        """
        @param servers e.g. "localhost:2181"
        """
        return ZKClient(servers,timeout)
        
    
    def createWatcher(name,methodToExecute):
        self.watchers[name]=""

"""Callable watcher that counts the number of notifications"""
class CountingWatcher(object):
    def __init__(self):
        self.count = 0

    def waitForExpected(self, count, maxwait):
        """Wait up to maxwait seconds for the specified count,
        return the count whether or not maxwait reached.

        Arguments:
        - `count`: expected count
        - `maxwait`: max seconds to wait
        """
        waited = 0
        while (waited < maxwait):
            if self.count >= count:
                return self.count
            time.sleep(1.0);
            waited += 1
        return self.count

    def __call__(self, handle, typ, state, path):
        self.count += 1
        print("handle %d got watch for %s in watcher, count %d" % (handle, path, self.count))

"""Callable watcher that counts the number of notifications
and verifies that the paths are sequential"""
class SequentialCountingWatcher(CountingWatcher):
    def __init__(self, child_path):
        CountingWatcher.__init__(self)
        self.child_path = child_path

    def __call__(self, handle, typ, state, path):
        if not self.child_path(self.count) == path:
            raise SmokeError("handle %d invalid path order %s" % (handle, path))
        CountingWatcher.__call__(self, handle, typ, state, path)

class Callback(object):
    def __init__(self):
        self.cv = threading.Condition()
        self.callback_flag = False
        self.rc = -1

    def callback(self, handle, rc, handler):
        self.cv.acquire()
        self.callback_flag = True
        self.handle = handle
        self.rc = rc
        handler()
        self.cv.notify()
        self.cv.release()

    def waitForSuccess(self, timeout=TIMEOUT):
        while not self.callback_flag:
            self.cv.wait(timeout)
        self.cv.release()

        if not self.callback_flag == True:
            raise SmokeError("asynchronous operation timed out on handle %d" %
                             (self.handle))
        if not self.rc == zookeeper.OK:
            raise SmokeError(
                "asynchronous operation failed on handle %d with rc %d" %
                (self.handle, self.rc))


class GetCallback(Callback):
    def __init__(self):
        Callback.__init__(self)

    def __call__(self, handle, rc, value, stat):
        def handler():
            self.value = value
            self.stat = stat
        self.callback(handle, rc, handler)

class SetCallback(Callback):
    def __init__(self):
        Callback.__init__(self)

    def __call__(self, handle, rc, stat):
        def handler():
            self.stat = stat
        self.callback(handle, rc, handler)

class CreateCallback(Callback):
    def __init__(self):
        Callback.__init__(self)

    def __call__(self, handle, rc, path):
        def handler():
            self.path = path
        self.callback(handle, rc, handler)

class DeleteCallback(Callback):
    def __init__(self):
        Callback.__init__(self)

    def __call__(self, handle, rc):
        def handler():
            pass
        self.callback(handle, rc, handler)

        
        
