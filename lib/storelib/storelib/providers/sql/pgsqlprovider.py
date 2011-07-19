from .. import IMonitorHistoryProvider
from conpool import SimpleConnectionPool
import pg
import os
import time

def connection(func):
    def wrapper(self, *args, **kwargs):
        connection = self.pool.getConnection()
        try:
            return func(self, connection, *args, **kwargs)
        finally:
            self.pool.releaseConnection(connection)
    return wrapper
    
class SQLProvider(IMonitorHistoryProvider):
    def __init__(self, hostname, username, password, dbname="monitorhistory", port=-1):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        
        self.pool = SimpleConnectionPool(10, hostname, port, username, password, dbname)
        self.__initialize()
        
    def __initialize(self):
        #initialize DB if needed
        con = pg.connect("postgres", self.hostname, self.port, user=self.username, passwd=self.password)
        try:
            exists = False
            res = con.query(""" SELECT count(datname) as "exists" FROM pg_database where datname = '%s'; """ % self.dbname)
            if res.dictresult()[0]['exists']:
                exists = True
            if exists:
                return
            con.query("""CREATE DATABASE "%s" """ % self.dbname)
            con.close()
            con = pg.connect(self.dbname, self.hostname, self.port, user=self.username, passwd=self.password)
            scehamafile = os.path.join(os.path.dirname(__file__), "schemas", "db.sql")
            with open(scehamafile) as f:
                query = f.read()
                con.query(query)
        finally:
            try:
                con.close()
            except:
                pass
    
    @connection
    def create(self, con, dsid):
        con.query("""SELECT store_create('%s');""" % pg.escape_string(dsid))
    
    @connection
    def destroy(self, con, dsid):
        con.query("""SELECT store_destroy('%s');""" % pg.escape_string(dsid))
    
    @connection
    def exists(self, con, dsid):
        result = con.query("""SELECT store_exists('%s') as exists;""" % pg.escape_string(dsid))
        
        rows = result.dictresult()
        return bool(rows[0]['exists'])
        
    @connection
    def save(self, con, dsid, *args):
        for pair in args:
            timestamp, value = pair
            con.query("SELECT store_save('%s', %d, %s)" % (pg.escape_string(dsid),
                                                           timestamp, 
                                                           value))
    
    @connection
    def getLatest(self, con, dsid):
        now = int(time.time())
        now = (now/300) * 300 #to align time
        #just try 2 periods
        for i in range(2):
            result = con.query("""SELECT store_get('%s', %d) as "value" """ % (dsid, now))
            rows = result.dictresult()
            if rows:
                row = rows[0]
                if row['value'] != None:
                    return float(row['value'])
            now -= 300
        return None
    
    @connection
    def getMin(self, con, dsid, starttime, endtime):
        result = con.query("""SELECT store_get_between('%(dsid)s', %(starttime)d, %(endtime)d, 'MIN') as "value" """ % {'dsid': dsid,
                                                                                                    'starttime': starttime,
                                                                                                    'endtime': endtime})
        rows = result.dictresult()
        if rows:
            v = rows[0]['value']
            return float(v) if v != None else v
        else:
            return None
    
    @connection
    def getMax(self, con, dsid, starttime, endtime):
        result = con.query("""SELECT store_get_between('%(dsid)s', %(starttime)d, %(endtime)d, 'MAX') as "value" """ % {'dsid': dsid,
                                                                                                    'starttime': starttime,
                                                                                                    'endtime': endtime})
        rows = result.dictresult()
        if rows:
            v = rows[0]['value']
            return float(v) if v != None else v
        else:
            return None
    
    @connection
    def getAverage(self, con, dsid, starttime, endtime):
        result = con.query("""SELECT store_get_between('%(dsid)s', %(starttime)d, %(endtime)d, 'AVG') as "value" """ % {'dsid': dsid,
                                                                                                    'starttime': starttime,
                                                                                                    'endtime': endtime})
        rows = result.dictresult()
        if rows:
            v = rows[0]['value']
            return float(v) if v != None else v
        else:
            return None
    
    @connection
    def getRange(self, con, dsid, resolution, starttime, endtime, aggregationfunction='AVG'):
        aggregationfunction = aggregationfunction.lower()
        if aggregationfunction not in ('avg', 'min', 'max'):
            raise ValueError("Invalid aggregation function '%s'" % aggregationfunction)
        result = con.query("""select * from get_range('%(dsid)s', %(resolution)d, %(starttime)d, %(endtime)d, '%(aggrfunc)s')
                     as data("timestamp" integer, "value" numeric);""" % {'dsid': dsid,
                                                                          'resolution': resolution,
                                                                          'starttime': starttime,
                                                                          'endtime': endtime,
                                                                          'aggrfunc': aggregationfunction})
        res = list()
        for row in result.dictresult():
            res.append((row['timestamp'], float(row['value']) if row['value'] else None))
        return res
    
    @connection
    def getGroupedLatest(self, con, dsids, groupfunction='ADD'):
        groupfunction = groupfunction.lower()
        if groupfunction not in ('add', 'avg', 'min', 'max'):
            raise ValueError("Invalid aggregation function '%s'" % groupfunction)

        now = int(time.time())
        now = (now/300) * 300 #to align time
        #just try 2 periods
        for i in range(2):
            result = con.query("""select * from get_grouped_latest(array[%(dsid)s], %(now)d, '%(aggrfunc)s')
                         as data("timestamp" integer, "value" numeric);""" % {'dsid': ", ".join(map(lambda x: "'%s'" % x, dsids)),
                                                                              'now': now,
                                                                              'aggrfunc': groupfunction})
            rows = result.dictresult()
            if rows:
                row = rows[0]
                if row['value'] != None:
                    return float(row['value'])
            now -= 300
        return None

    @connection
    def getGroupedMin(self, con, dsids, resolution, starttime, endtime, groupfunction='ADD'):
        groupfunction = groupfunction.lower()
        if groupfunction not in ('add', 'avg', 'min', 'max'):
            raise ValueError("Invalid aggregation function '%s'" % groupfunction)
        
        result = con.query("""select min("value") as "value" from get_grouped_range(array[%(dsid)s], %(resolution)d, %(starttime)d, %(endtime)d, '%(aggrfunc)s')
                     as data("timestamp" integer, "value" numeric);""" % {'dsid': ", ".join(map(lambda x: "'%s'" % x, dsids)),
                                                                          'resolution': resolution,
                                                                          'starttime': starttime,
                                                                          'endtime': endtime,
                                                                          'aggrfunc': groupfunction})
        rows = result.dictresult()
        if rows:
            v = rows[0]['value']
            return float(v if v != None else 0)
        else:
            return None
    
    @connection
    def getGroupedMax(self, con, dsids, resolution, starttime, endtime, groupfunction='ADD'):
        groupfunction = groupfunction.lower()
        if groupfunction not in ('add', 'avg', 'min', 'max'):
            raise ValueError("Invalid aggregation function '%s'" % groupfunction)
        
        result = con.query("""select max("value") as "value" from get_grouped_range(array[%(dsid)s], %(resolution)d, %(starttime)d, %(endtime)d, '%(aggrfunc)s')
                     as data("timestamp" integer, "value" numeric);""" % {'dsid': ", ".join(map(lambda x: "'%s'" % x, dsids)),
                                                                          'resolution': resolution,
                                                                          'starttime': starttime,
                                                                          'endtime': endtime,
                                                                          'aggrfunc': groupfunction})
        rows = result.dictresult()
        if rows:
            v = rows[0]['value']
            return float(v if v != None else 0)
        else:
            return None
    
    @connection
    def getGroupedAvg(self, con, dsids, resolution, starttime, endtime, groupfunction='ADD'):
        groupfunction = groupfunction.lower()
        if groupfunction not in ('add', 'avg', 'min', 'max'):
            raise ValueError("Invalid aggregation function '%s'" % groupfunction)
        
        result = con.query("""select avg("value") as "value" from get_grouped_range(array[%(dsid)s], %(resolution)d, %(starttime)d, %(endtime)d, '%(aggrfunc)s')
                     as data("timestamp" integer, "value" numeric);""" % {'dsid': ", ".join(map(lambda x: "'%s'" % x, dsids)),
                                                                          'resolution': resolution,
                                                                          'starttime': starttime,
                                                                          'endtime': endtime,
                                                                          'aggrfunc': groupfunction})
        rows = result.dictresult()
        if rows:
            v = rows[0]['value']
            return float(v if v != None else 0)
        else:
            return None
    
    @connection
    def getGroupedRange(self, con, dsids, resolution, starttime, endtime, groupfunction='ADD'):
        groupfunction = groupfunction.lower()
        if groupfunction not in ('add', 'avg', 'min', 'max'):
            raise ValueError("Invalid aggregation function '%s'" % groupfunction)
        
        result = con.query("""select * from get_grouped_range(array[%(dsid)s], %(resolution)d, %(starttime)d, %(endtime)d, '%(aggrfunc)s')
                     as data("timestamp" integer, "value" numeric);""" % {'dsid': ", ".join(map(lambda x: "'%s'" % x, dsids)),
                                                                          'resolution': resolution,
                                                                          'starttime': starttime,
                                                                          'endtime': endtime,
                                                                          'aggrfunc': groupfunction})
        res = list()
        for row in result.dictresult():
            res.append((row['timestamp'], float(row['value']) if row['value'] else None))
        return res
    