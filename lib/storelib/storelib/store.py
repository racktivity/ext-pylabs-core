import os
import providers
import time
import re
import imp
import threading

class storewrapper(providers.IMonitorHistoryProvider):
    def __init__(self, provider):
        self.__provider = provider
    
    def __processtimes(self, start, end, resolution):
        start = str(start).lower()
        end = str(end).lower()
        startv = None
        endv = None
        now = int(time.time())
        
        align = lambda t: (int(t)/resolution) * resolution
        
        if start == "now":
            start = str(now)
        if end == "now":
            end = str(now)
        
        if start.isdigit():
            startv = int(start)
        if end.isdigit():
            endv = int(end)
        
        if startv == None and endv == None:
            raise ValueError("Start and End time are both relative '%s' - '%s'" % (start, end))
        elif startv != None and endv != None:
            return align(startv), align(endv)
        
        p = re.compile("^(\w)?([+-])(\d+)(\w)?$")
        HOUR = 60 * 60
        DAY = 24 * HOUR
        WEEK = 7 * DAY
        MONTH = 4 * WEEK
        YEAR = 12 * MONTH
        
        relativeRange = {'h': HOUR,
                         'd': DAY,
                         'w': WEEK,
                         'm': MONTH,
                         'y': YEAR,
                         '' : 1}
        
        relativeTo = {'e': endv,
                      's': startv,
                      '': now}
        
        operations = {'+': lambda a,b: a + b,
                      '-': lambda a,b: a - b}
        
        if not startv:
            #start is relative.
            m = p.match(start)
            if not m:
                raise ValueError("Invalid relative pattern '%s'" % start)
            base = m.group(1)
            
            if base not in relativeTo:
                raise ValueError("Invalid relative base '%s' in '%s'" % (base, start))
            
            basevalue = relativeTo[base]
            if not basevalue:
                raise ValueError("Time is relative to itself, this can't be")
            
            range = m.group(4)
            if range not in relativeRange:
                raise ValueError("Invalid relative range '%s' in '%s'" % (range, start))
            
            rangevalue =  relativeRange[range]
            diffvalue = int(m.group(3))
            op = m.group(2)
            
            startv = operations[op](basevalue, diffvalue * rangevalue)
        
        if not endv:
            #start is relative.
            m = p.match(end)
            if not m:
                raise ValueError("Invalid relative pattern '%s'" % start)
            base = m.group(1)
            
            if base not in relativeTo:
                raise ValueError("Invalid relative base '%s' in '%s'" % (base, end))
            
            basevalue = relativeTo[base]
            if not basevalue:
                raise ValueError("Time is relative to itself, this can't be")
            
            range = m.group(4)
            if range not in relativeRange:
                raise ValueError("Invalid relative range '%s' in '%s'" % (range, end))
            
            rangevalue =  relativeRange[range]
            diffvalue = int(m.group(3))
            op = m.group(2)
            
            endv = operations[op](basevalue, diffvalue * rangevalue)
            
        return align(startv), align(endv)
            
    def create(self, dsid):
        return self.__provider.create(dsid)
    
    def destroy(self, dsid):
        return self.__provider.destroy(dsid)
    
    def exists(self, dsid):
        return self.__provider.exists(dsid)
    
    def save(self, dsid, *args):
        align = lambda t: (int(t)/300) * 300
        values = []
        for t, v in args:
            values.append((align(t), v))
        return self.__provider.save(dsid, *values)
    
    def getLatest(self, dsid):
        return self.__provider.getLatest(dsid)
    
    def getMin(self, dsid, starttime="e-1d", endtime="now"):
        starttime, endtime = self.__processtimes(starttime, endtime, 300)
        return self.__provider.getMin(dsid, starttime, endtime)
    
    def getMax(self, dsid, starttime="e-1d", endtime="now"):
        starttime, endtime = self.__processtimes(starttime, endtime, 300)
        return self.__provider.getMax(dsid, starttime, endtime)
    
    def getAverage(self, dsid, starttime="e-1d", endtime="now"):
        starttime, endtime = self.__processtimes(starttime, endtime, 300)
        return self.__provider.getAverage(dsid, starttime, endtime)
    
    def getRange(self, dsid, resolution, starttime="e-1d", endtime="now", aggregationfunction='AVG'):
        starttime, endtime = self.__processtimes(starttime, endtime, resolution)
        return self.__provider.getRange(dsid, resolution, starttime, endtime, aggregationfunction)
    
    def getGroupedLatest(self, dsids, groupfunction='ADD'):
        return self.__provider.getGroupedLatest(dsids, groupfunction)
    
    def getGroupedMin(self, dsids, resolution, starttime="e-1d", endtime="now", groupfunction='ADD'):
        starttime, endtime = self.__processtimes(starttime, endtime, resolution)
        return self.__provider.getGroupedMin(dsids, resolution, starttime, endtime, groupfunction)
    
    def getGroupedMax(self, dsids, resolution, starttime="e-1d", endtime="now", groupfunction='ADD'):
        starttime, endtime = self.__processtimes(starttime, endtime, resolution)
        return self.__provider.getGroupedMax(dsids, resolution, starttime, endtime, groupfunction)
    
    def getGroupedAvg(self, dsids, resolution, starttime="e-1d", endtime="now", groupfunction='ADD'):
        starttime, endtime = self.__processtimes(starttime, endtime, resolution)
        return self.__provider.getGroupedAvg(dsids, resolution, starttime, endtime, groupfunction)
    
    def getGroupedRange(self, dsids, resolution, starttime="e-1d", endtime="now", groupfunction='ADD'):
        starttime, endtime = self.__processtimes(starttime, endtime, resolution)
        return self.__provider.getGroupedRange(dsids, resolution, starttime, endtime, groupfunction)
    
    
__mutex = threading.RLock()
__store = {}

def factory(providername, **params):
    def _getprovider(providername):
        providersdir = os.path.join(os.path.dirname(__file__),
                                "providers")
        candidates = os.listdir(providersdir)
        providerclass = None
        for candidate in candidates:
            if not os.path.isdir(os.path.join(providersdir, candidate)):
                continue
            if not os.path.exists(os.path.join(providersdir, candidate, "__init__.py")):
                continue
            
            if candidate != providername:
                continue
            actionmod = __import__("storelib.providers.%s" % candidate, fromlist=[candidate], level=1)
            if hasattr(actionmod, 'PROVIDERCLASS'):
                providerclass = getattr(actionmod, 'PROVIDERCLASS')
            
        return providerclass
    
    __mutex.acquire()
    try:
        if providername in __store:
            return __store[providername]
        
        providerclass = _getprovider(providername)
        if not providerclass:
            raise ValueError("Can't find a valid providername with name '%s'" % providername)
            
        provider = storewrapper(providerclass(**params))
        __store[providername] = provider
        
        return provider
    finally:
        __mutex.release()

CONFIG_TYPE = "storelib"

def cfgfactory():
    from pylabs import q
    config = q.config.getConfig(CONFIG_TYPE)
    if 'main' not in config:
        raise RuntimeError("Failed to start the store service, no main section in %s.cfg" % CONFIG_TYPE)
    maincfg = config['main']
    if 'store' not in maincfg:
        raise RuntimeError("Missing required config parameter 'store' and the %s.cfg main section" % CONFIG_TYPE)
    
    store = maincfg['store']
    params = config.get(store, {})
    
    return factory(store, **params)