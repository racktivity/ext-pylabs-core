#!/usr/bin/python
# -*- coding: utf-8 -*-
import mysql2cache
import sqlite3
from racktivity.common.GUIDLoader import Value
import sys

con = sqlite3.connect(":memory:")
mysql2cache.generateDB(con)

#Load the modules types we have (Power/Temprature/Master)
moduleNames = []
for (mod,) in con.execute("select distinct type from modules"):
    moduleNames.append(mod)

print """from racktivity.sal.proxy import connection
from racktivity.common.GUIDTable import Value
from racktivity.common import convert

class RackSal(object):

    def __init__(self, username, password, hostname, port, format="R"):
        self._client = connection.Connect(username, password, hostname, port, format)
        self._format = format"""

#load the guid table
first=True
print "        self._guidTable = {"
for (guid, valDefRaw) in con.execute('select guid,valDef from tbl_guid'):
    print "             " + str(guid) + ":" + "Value(%s),"%repr(valDefRaw)
print "        }"
    
for mod in moduleNames:
    print "        self.%s = %s(self)"%(mod,mod.capitalize())    
print """
    def _getObjectFromData(self, data, valDef, setter=False, count=1):
        if self._format == "R" and not setter:
            if count == 1:
                return convert.bin2value(data,valDef)
            if data[0] != "\\0": #This is an error code, return it
                return convert.bin2value(data,valDef)
            #Remove the error byte
            data = data[1:]
            #get length of each port
            length = len(data)/count
            #Split the ports
            dataList = convert.sliceString(data, length)
            result = []
            for data in dataList:
                result.append(convert.bin2value(data,valDef,checkErrorByte=False)[1])
            return 0,result
        else:
            if data and data.find(":"):
                errorcode, data = data.split(":", 1)
            else:
                return data, None
            if setter:
                return int(data)
            return errorcode, convert.ascii2emu(data, valDef)[1]
"""

for mod in moduleNames:
    print """class %s(object):
    def __init__(self, parent):
        self._parent = parent
        
    """%mod.capitalize()
    for (guid, name, valDefRaw, read, write, comment, count) in con.execute('select tbl_guid.*,modules.count from tbl_guid,modules where modules.guid = tbl_guid.guid and modules.type="%s"'% mod):
        valDef = Value(valDefRaw)
        if valDef.type == "pointer": continue #Pointer has their own special function

        params = ""
        vars = []
        
        if mod == "master":
            vars.append("moduleID = 'M1'")
        else:
            params += ", moduleID"
        
        params += ", value"
        if count > 1:
            params += ", portnumber=1, length=1"
        else:
            vars.append("portnumber=1")
            vars.append("length=1")
        
        print "    #Attribute '" + name + "' GUID ", guid, "Data type", valDef.type
	if comment and (read or write):
            print "    #%s" % comment
        if read:
            print "    def get" + name + "(self" + params.replace(", value","") + "):"
            print "        guid = ", guid
            for var in vars:
                print "        " + var
            print "        valDef = self._parent._guidTable[guid]"
            print "        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)"
            print "        return self._parent._getObjectFromData(data, valDef, count=length)"
            print "        "
        
        if write:
            params = params.replace("length=1","")
            
            print "    def set" + name + "(self" + params + "):"
            print "        guid = ", guid
            for var in vars:
                print "        " + var            
            print "        valDef = self._parent._guidTable[guid]"
            if valDef.type == "number":
                print "        data = self._parent._client.setAttribute(moduleID, guid, int(round(value * %d)), portnumber)"%(10 ** valDef.scale)
            else:
                print "        data = self._parent._client.setAttribute(moduleID, guid, value, portnumber)"
            print "        return self._parent._getObjectFromData(data, valDef, setter=True)"
            print "        "
    #Look for troubles, look for pointers
    print "    #The pointers!!"
    for (guid, name) in con.execute('select guid,name from tbl_guid where name in (select distinct name from modules where type="%s")'% mod):
            if mod == "master":
                print "    def get" + name + "(self):"
                print "        moduleID='M1'"
            else:
                print "    def get" + name + "(self, moduleID):"
            print "        guid = ", guid
            print "        paramInfo = ["
            for (pGuid,pCount) in con.execute('select guid,count from modules where type=? and name=? order by id',(mod, name)):
                sys.stdout.write("        (self._parent._guidTable[%d],%d),\n"%(pGuid,pCount))
            print "        ]"
            print """      
        #Get pointer's data
        data = self._parent._client.getAttribute(moduleID, guid)
        return convert.pointer2values(data, paramInfo)
        """
con.close()
sys.stderr.write("Done, don't forget to run GUIDGenerator.py\n")
