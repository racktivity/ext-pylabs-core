import pg
import time
import os
from pylabs import q,p
import pylabs

class Logger:
    conn = None
    def init(self):
        self.conn = None
        self.conn = p.application.getOsisConnection(p.api.appname)
    
    def __del__(self):
        if self.conn:
            self.conn.close()
    
    def log(self, request, model, guid, name, action, modifiedValues = None):
        if not self.conn:
            self.init()
        user = request["username"]
        ip = request["ipaddress"]
        #try to construct argument in key/value pairs
        timestamp = time.time()
        values = "("
        for value in (user, ip, model, guid, name, action, timestamp):
            
            if value is None:
                values += " NULL"
            elif isinstance(value, str):
                 values += "'%s'"%pg.escape_string(value)
            else:
                values += "%s"%value
            values += ","
        values = values[:-1] + ")"
        self.conn.runQuery('INSERT INTO audit("user","ip", "model", "guid", "name", "action", "timestamp") values %s'%values)
        
        if modifiedValues:
            id = self.conn.runQuery("select last_value from audit_id_seq").getresult()[0][0]
            for modifiedValue in modifiedValues:
                mvName = modifiedValue["name"]
                mvOld =  repr(modifiedValue["old"])
                mvNew =  repr(modifiedValue["new"])
                self.conn.runQuery("""INSERT INTO values("eventId", "valName", "old", "new") values(%d, '%s', '%s', '%s')""" % (id,
                                                                                                                             pg.escape_string(mvName),
                                                                                                                             pg.escape_string(mvOld),
                                                                                                                             pg.escape_string(mvNew)))
            
    
    def log_tasklet(self, tags, params, modifiedKeys = (), nameKey = "name"):
        """
          tags is the __tags__ variable
          params is the params variable
          modifiedKeys is a tuple of names of attributes that can be modified
          nameKey is the attribute that holds the objects name
        """
        model = tags[0]
        action = tags[1]
        guid = name = previousVal = newVal = None
        if "guid" in params:
            guid = params["guid"]
        elif model + "guid" in params:
            guid = params[model + "guid"]
        
        if guid:
            drpobj = getattr(q.drp, model)
            obj = drpobj.get(guid)
            name = getattr(obj, nameKey)
        elif nameKey in params:
            name = params[nameKey]
        
        modifiedValues = list()
        if modifiedKeys:
            drpObj = getattr(q.drp, model)
            obj = drpobj.get(guid)
            for mkey in modifiedKeys:
                newVal = params[mkey]
                if newVal is None:
                    continue
                oldVal = getattr(obj, mkey)
                if isinstance(oldVal, pylabs.baseclasses.BaseEnumeration):
                    oldVal = str(oldVal)
                if newVal == "" or oldVal == newVal:
                    continue
                valDict = {"name":mkey, "old":oldVal, "new":newVal}
                modifiedValues.append(valDict)
        self.log(params["request"], model, guid, name, action, modifiedValues)
    
logger = Logger()
