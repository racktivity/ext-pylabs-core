import pg
import threading

class SimpleConnectionPool(object):
    def __init__(self, poolsize, hostname, port, username, password, dbname):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        
        self.__poolsize = poolsize
        self.__available = list()
        self.__out = list()
        self.__mutex = threading.Condition()
    
    def getConnection(self):
        """
        Get connection from the pool, create one if needed or waith until another connection is released
        """
        self.__mutex.acquire()
        try:
            while not len(self.__available):
                total = len(self.__available) + len(self.__out)
                if total < self.__poolsize:
                    #create a new connection
                    con = pg.connect(self.dbname, self.hostname, self.port, user=self.username, passwd=self.password)
                    self.__out.append(con)
                    return con
                else:
                    #the pool is full, we should wait until a connection is released
                    self.__mutex.wait()
            
            #A connection is available. just pop it out
            con = self.__available.pop()
            self.__out.append(con)
            
            return con
        finally:
            self.__mutex.release()
    
    def releaseConnection(self, connection):
        """
        Return a connection to the pool
        """
        self.__mutex.acquire()
        try:
            self.__out.remove(connection)
            self.__available.append(connection)
        finally:
            self.__mutex.release()