from racktivity.sal.proxy import connection
from racktivity.common.GUIDTable import Value
from racktivity.common import convert

class RackSal(object):

    def __init__(self, username, password, hostname, port, format="R"):
        self._client = connection.Connect(username, password, hostname, port, format)
        self._format = format
        self._guidTable = {
             1:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit=''\nscale=0L"),
             2:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             3:Value(u"type='TYPE_TIMESTAMP'\nsize=4L\nlength=4L\nunit='UNIX'\nscale=0L"),
             4:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='V'\nscale=2L"),
             5:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='Hz'\nscale=3L"),
             6:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='A'\nscale=3L"),
             7:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='W'\nscale=1L"),
             8:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             9:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit='kWh'\nscale=3L"),
             10:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit='kVAh'\nscale=3L"),
             11:Value(u"type='TYPE_SIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='C'\nscale=1L"),
             12:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='%RH'\nscale=1L"),
             13:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='rpm'\nscale=0L"),
             14:Value(u"type='TYPE_IP'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             15:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='VA'\nscale=1L"),
             16:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit='%'\nscale=0L"),
             17:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='A'\nscale=3L"),
             18:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit='W'\nscale=1L"),
             19:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit='VA'\nscale=1L"),
             20:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit='kWh'\nscale=3L"),
             21:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit='kVAh'\nscale=3L"),
             22:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit='%'\nscale=0L"),
             5000:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='A'\nscale=3L"),
             5001:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='W'\nscale=1L"),
             5002:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='A'\nscale=3L"),
             5003:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=8L\nlength=8L\nunit='W'\nscale=1L"),
             5004:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='V'\nscale=2L"),
             5005:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='V'\nscale=2L"),
             5006:Value(u"type='TYPE_SIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='C'\nscale=1L"),
             5007:Value(u"type='TYPE_SIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='C'\nscale=1L"),
             5008:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='%RH'\nscale=1L"),
             5009:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='%RH'\nscale=1L"),
             5010:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='A'\nscale=3L"),
             5011:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='W'\nscale=1L"),
             5012:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=5L\nlength=5L\nunit='%'\nscale=0L"),
             5013:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=5L\nlength=5L\nunit='%'\nscale=0L"),
             5014:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='A'\nscale=3L"),
             5015:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=6L\nlength=6L\nunit='W'\nscale=1L"),
             5016:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=5L\nlength=5L\nunit='%'\nscale=0L"),
             5017:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=5L\nlength=5L\nunit='%'\nscale=0L"),
             10000:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10001:Value(u"type='TYPE_STRING'\nsize=32L\nlength=32L\nunit=''\nscale=0L"),
             10002:Value(u"type='TYPE_VERSION'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10003:Value(u"type='TYPE_VERSION'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10004:Value(u"type='TYPE_STRING'\nsize=8L\nlength=8L\nunit=''\nscale=0L"),
             10005:Value(u"type='TYPE_STRING'\nsize=8L\nlength=8L\nunit=''\nscale=0L"),
             10006:Value(u"type='TYPE_STRING'\nsize=32L\nlength=32L\nunit=''\nscale=0L"),
             10007:Value(u"type='TYPE_STRING'\nsize=32L\nlength=32L\nunit=''\nscale=0L"),
             10008:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10009:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10010:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10011:Value(u"type='TYPE_IP'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10012:Value(u"type='TYPE_SUBNETMASK'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10013:Value(u"type='TYPE_IP'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10014:Value(u"type='TYPE_IP'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10015:Value(u"type='TYPE_MAC'\nsize=6L\nlength=6L\nunit=''\nscale=0L"),
             10016:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10017:Value(u"type='TYPE_IP'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10018:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10019:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10020:Value(u"type='TYPE_IP'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10021:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit=''\nscale=0L"),
             10022:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10023:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10024:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10025:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit=''\nscale=0L"),
             10026:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit=''\nscale=0L"),
             10027:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10028:Value(u"type='TYPE_IP'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10029:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10030:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit='s'\nscale=0L"),
             10031:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10032:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit='min'\nscale=0L"),
             10033:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10034:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10035:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10036:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit='1H8L'\nscale=0L"),
             10037:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='s'\nscale=0L"),
             10038:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='A'\nscale=3L"),
             10039:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='A'\nscale=3L"),
             10040:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='W'\nscale=1L"),
             10041:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='W'\nscale=1L"),
             10042:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='A'\nscale=3L"),
             10043:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='A'\nscale=3L"),
             10044:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='W'\nscale=1L"),
             10045:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='W'\nscale=1L"),
             10046:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='V'\nscale=2L"),
             10047:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='V'\nscale=2L"),
             10048:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='V'\nscale=2L"),
             10049:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='V'\nscale=2L"),
             10050:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=8L\nlength=8L\nunit='kWh'\nscale=3L"),
             10051:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=8L\nlength=8L\nunit='kVAh'\nscale=3L"),
             10052:Value(u"type='TYPE_SIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='C'\nscale=1L"),
             10053:Value(u"type='TYPE_SIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='C'\nscale=1L"),
             10054:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='%RH'\nscale=1L"),
             10055:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit='%RH'\nscale=1L"),
             10056:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10057:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10058:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10059:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10060:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10061:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
             10062:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             10063:Value(u"type='TYPE_SIGNED_NUMBER'\nsize=2L\nlength=2L\nunit=''\nscale=1L"),
             10064:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit='%'\nscale=0L"),
             10065:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit='%'\nscale=0L"),
             10066:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=4L\nlength=4L\nunit='s'\nscale=0L"),
             10067:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10068:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10069:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10070:Value(u"type='TYPE_STRING'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             10071:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=8L\nlength=8L\nunit='kWh'\nscale=3L"),
             10072:Value(u"type='TYPE_UNSIGNED_NUMBER_WITH_TS'\nsize=8L\nlength=8L\nunit='kVAh'\nscale=3L"),
             40000:Value(u"type='TYPE_COMMAND'\nsize=0L\nlength=0L\nunit=''\nscale=0L"),
             40001:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40002:Value(u"type='TYPE_COMMAND'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             40003:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40004:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40005:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40006:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40007:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40008:Value(u"type='TYPE_COMMAND'\nsize=26L\nlength=26L\nunit=''\nscale=0L"),
             40009:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40010:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40011:Value(u"type='TYPE_ENUM'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40012:Value(u"type='TYPE_STRING'\nsize=32L\nlength=32L\nunit=''\nscale=0L"),
             40013:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40014:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             40015:Value(u"type='TYPE_COMMAND'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50000:Value(u"type='TYPE_POINTER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50001:Value(u"type='TYPE_POINTER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50002:Value(u"type='TYPE_CIRCULAR_BUFFER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50003:Value(u"type='TYPE_CIRCULAR_BUFFER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50004:Value(u"type='TYPE_RAW'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50005:Value(u"type='TYPE_RAW'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50006:Value(u"type='TYPE_RAW'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50007:Value(u"type='TYPE_RAW'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50008:Value(u"type='TYPE_RAW'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50009:Value(u"type='TYPE_RAW'\nsize=2L\nlength=2L\nunit=''\nscale=0L"),
             50010:Value(u"type='TYPE_POINTER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             50011:Value(u"type='TYPE_RAW'\nsize=16L\nlength=16L\nunit=''\nscale=0L"),
             60000:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             60001:Value(u"type='TYPE_COMMAND'\nsize=0L\nlength=0L\nunit=''\nscale=0L"),
             60002:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             60004:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit=''\nscale=0L"),
             60005:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=2L\nlength=2L\nunit=''\nscale=0L"),
             60010:Value(u"type='TYPE_UNSIGNED_NUMBER'\nsize=1L\nlength=1L\nunit=''\nscale=0L"),
             60020:Value(u"type='TYPE_STRING'\nsize=8L\nlength=8L\nunit=''\nscale=0L"),
             60021:Value(u"type='TYPE_VERSION'\nsize=4L\nlength=4L\nunit=''\nscale=0L"),
        }
        self.master = Master(self)
        self.power = Power(self)

    def _getObjectFromData(self, data, valDef, setter=False, count=1):
        if self._format == "R":
            if setter:
                return convert.bin2int(data)
            if count == 1:
                return convert.bin2value(data,valDef)
            if data[0] != "\0": #This is an error code, return it
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

class Master(object):
    def __init__(self, parent):
        self._parent = parent
        
    #Attribute 'CurrentTime' GUID  3 Data type TYPE_TIMESTAMP
    #Unix timestamp of the current time
    def getCurrentTime(self):
        guid =  3
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
    
    #Attribute 'Temperature' GUID  11 Data type TYPE_SIGNED_NUMBER
    #Temperature
    def getTemperature(self):
        guid =  11
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
    
    def getMinTemperature(self):
        guid =  5006
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MaxTemperature' GUID  5007 Data type TYPE_SIGNED_NUMBER_WITH_TS
    #Maximum temperature occurred since last reset
    def getMaxTemperature(self):
        guid =  5007
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
    
    #Attribute 'AdminLogin' GUID 10067 Data type TYPE_STRING
    def getUserLogin(self):
        guid =  10067
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setUserLogin(self, value):
        guid =  10067
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)

    #Attribute 'AdminLogin' GUID 10069 Data type TYPE_STRING
    def getRestrictedUserLogin(self):
        guid =  10069
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setRestrictedUserLogin(self, value):
        guid =  10069
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
    
    #Attribute 'AdminLogin' GUID 10008 Data type TYPE_STRING
    def getAdminLogin(self):
        guid =  10008
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setAdminLogin(self, value):
        guid =  10008
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)

    #Attribute 'AdminPassword' GUID  10009 Data type TYPE_STRING
    def getAdminPassword(self):
        guid =  10009
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setAdminPassword(self, value):
        guid =  10009
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)

    #Attribute 'Address' GUID  10000 Data type TYPE_UNSIGNED_NUMBER
    #Identification of the module
    def getAddress(self, portnumber=1, length=1):
        guid =  10000
        moduleID = 'M1'
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'ModuleName' GUID  10001 Data type TYPE_STRING
    #Module name
    def getModuleName(self):
        guid =  10001
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'FirmwareVersion' GUID  10002 Data type TYPE_VERSION
    #Firmware version
    def getFirmwareVersion(self):
        guid =  10002
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'HardwareVersion' GUID  10003 Data type TYPE_VERSION
    #Hardware version
    def getHardwareVersion(self):
        guid =  10003
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'FirmwareID' GUID  10004 Data type TYPE_STRING
    #Identification of the firmware
    def getFirmwareID(self):
        guid =  10004
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'HardwareID' GUID  10005 Data type TYPE_STRING
    #Identification of the hardware
    def getHardwareID(self):
        guid =  10005
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'RackName' GUID  10006 Data type TYPE_STRING
    #Rack Name
    def getRackName(self):
        guid =  10006
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setRackName(self, value):
        guid =  10006
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'RackPosition' GUID  10007 Data type TYPE_STRING
    #Position of the PDU in the rack
    def getRackPosition(self):
        guid =  10007
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setRackPosition(self, value):
        guid =  10007
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'DoHotReset' GUID  40014 Data type TYPE_COMMAND
    #Hot reset of the device
    def setDoHotReset(self, value):
        guid =  40014
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'TemperatureUnitSelector' GUID  10010 Data type TYPE_ENUM
    def getTemperatureUnitSelector(self):
        guid =  10010
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setTemperatureUnitSelector(self, value):
        guid =  10010
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'IPAddress' GUID  10011 Data type TYPE_IP
    #IP-address
    def getIPAddress(self):
        guid =  10011
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setIPAddress(self, value):
        guid =  10011
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'SubNetMask' GUID  10012 Data type TYPE_SUBNETMASK
    #Subnetmask
    def getSubNetMask(self):
        guid =  10012
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setSubNetMask(self, value):
        guid =  10012
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'StdGateWay' GUID  10013 Data type TYPE_IP
    #Standard gateway IP
    def getStdGateWay(self):
        guid =  10013
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setStdGateWay(self, value):
        guid =  10013
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'DnsServer' GUID  10014 Data type TYPE_IP
    #Dns server IP
    def getDnsServer(self):
        guid =  10014
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setDnsServer(self, value):
        guid =  10014
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MAC' GUID  10015 Data type TYPE_MAC
    #MAC address
    def getMAC(self):
        guid =  10015
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'DHCPEnable' GUID  10016 Data type TYPE_ENUM
    #DHCP enable
    def getDHCPEnable(self):
        guid =  10016
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setDHCPEnable(self, value):
        guid =  10016
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'NTPServer' GUID  10017 Data type TYPE_IP
    #NTP server IP
    def getNTPServer(self):
        guid =  10017
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setNTPServer(self, value):
        guid =  10017
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'UseDefaultNTPServer' GUID  10018 Data type TYPE_ENUM
    def getUseDefaultNTPServer(self):
        guid =  10018
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setUseDefaultNTPServer(self, value):
        guid =  10018
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'UseNTP' GUID  10019 Data type TYPE_ENUM
    def setUseNTP(self, value):
        guid =  10019
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'SNMPTrapRecvIP' GUID  10020 Data type TYPE_IP
    #SNMP trap server IP-address
    def getSNMPTrapRecvIP(self):
        guid =  10020
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setSNMPTrapRecvIP(self, value):
        guid =  10020
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'SNMPTrapRecvPort' GUID  10021 Data type TYPE_UNSIGNED_NUMBER
    def getSNMPTrapRecvPort(self):
        guid =  10021
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setSNMPTrapRecvPort(self, value):
        guid =  10021
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'SNMPCommunityRead' GUID  10022 Data type TYPE_STRING
    def getSNMPCommunityRead(self):
        guid =  10022
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setSNMPCommunityRead(self, value):
        guid =  10022
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'SNMPCommunityWrite' GUID  10023 Data type TYPE_STRING
    def getSNMPCommunityWrite(self):
        guid =  10023
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setSNMPCommunityWrite(self, value):
        guid =  10023
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'SNMPControl' GUID  10024 Data type TYPE_ENUM
    def getSNMPControl(self):
        guid =  10024
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setSNMPControl(self, value):
        guid =  10024
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'LDAPServer' GUID  10028 Data type TYPE_IP
    def getLDAPServer(self):
        guid =  10028
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setLDAPServer(self, value):
        guid =  10028
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'UseLDAPServer' GUID  10029 Data type TYPE_ENUM
    def setUseLDAPServer(self, value):
        guid =  10029
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'Beeper' GUID  10030 Data type TYPE_UNSIGNED_NUMBER
    #Beeper control enable beeper for n seconds
    def getBeeper(self):
        guid =  10030
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setBeeper(self, value):
        guid =  10030
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'DisplayLock' GUID  10031 Data type TYPE_ENUM
    def getDisplayLock(self):
        guid =  10031
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setDisplayLock(self, value):
        guid =  10031
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'DisplayTimeOn' GUID  10032 Data type TYPE_UNSIGNED_NUMBER
    def getDisplayTimeOn(self):
        guid =  10032
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setDisplayTimeOn(self, value):
        guid =  10032
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'DisplayRotation' GUID  10033 Data type TYPE_ENUM
    def getDisplayRotation(self):
        guid =  10033
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setDisplayRotation(self, value):
        guid =  10033
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinTemperatureWarning' GUID  10052 Data type TYPE_SIGNED_NUMBER
    def getMinTemperatureWarning(self):
        guid =  10052
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinTemperatureWarning(self, value):
        guid =  10052
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxTemperatureWarning' GUID  10053 Data type TYPE_SIGNED_NUMBER
    def getMaxTemperatureWarning(self):
        guid =  10053
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxTemperatureWarning(self, value):
        guid =  10053
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'Startuptime' GUID  10066 Data type TYPE_UNSIGNED_NUMBER
    def getStartuptime(self):
        guid =  10066
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'JumpBoot' GUID  40000 Data type TYPE_COMMAND
    #Enter bootloader mode. Normally this command is only sent to application program. When the bootloader is already running, this command will only reply a positive acknowledge.
    def getJumpBoot(self):
        guid =  40000
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setJumpBoot(self, value):
        guid =  40000
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'GotoFactoryMode' GUID  40002 Data type TYPE_COMMAND
    def setGotoFactoryMode(self, value):
        guid =  40002
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'ModNum' GUID  40007 Data type TYPE_UNSIGNED_NUMBER
    #To retrieve the number of modules connected to the device. The device itself is treated as module 0.
    def getModNum(self):
        guid =  40007
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'ModInfo' GUID  40008 Data type TYPE_COMMAND
    def getModInfo(self, portnumber=1, length=1):
        guid =  40008
        moduleID = 'M1'
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'ApplyIPSettings' GUID  40009 Data type TYPE_COMMAND
    def setApplyIPSettings(self, value):
        guid =  40009
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'Monitor' GUID  50000 Data type TYPE_POINTER
    #Get the monitor values
    def getMonitor(self):
        guid =  50000
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Parameter' GUID  50001 Data type TYPE_POINTER
    #get all parameters
    def getParameter(self):
        guid =  50001
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'DHCPReset' GUID  40010 Data type TYPE_COMMAND
    #Reset DHCP
    def setDHCPReset(self, value):
        guid =  40010
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'CurrentIP' GUID  14 Data type TYPE_IP
    #Gives the current IP. When DHCP is on, you can see here what ip is given by the DHCP server
    def getCurrentIP(self):
        guid =  14
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'UDPUser' GUID  40013 Data type TYPE_COMMAND
    #User mode for UDP commands
    def setUDPUser(self, value):
        guid =  40013
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
     
    #Attribute 'TotalCurrent' GUID  17 Data type TYPE_UNSIGNED_NUMBER
    #Total current
    def getTotalCurrent(self):
        guid =  17
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TotalRealPower' GUID  18 Data type TYPE_UNSIGNED_NUMBER
    #Total real power
    def getTotalRealPower(self):
        guid =  18
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TotalActiveEnergy' GUID  20 Data type TYPE_UNSIGNED_NUMBER
    #Total active energy
    def getTotalActiveEnergy(self):
        guid =  20
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MonitorAutoRefresh' GUID  50010 Data type TYPE_POINTER
    #Get the monitor values from the module that are auto refreshed
    def getMonitorAutoRefresh(self):
        guid =  50010
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Role' GUID  40011 Data type TYPE_ENUM
    #To see in which role you are logged in
    def getRole(self):
        guid =  40011
        moduleID = 'M1'
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #The pointers!!
class Power(object):
    def __init__(self, parent):
        self._parent = parent
        
    #Attribute 'CurrentTime' GUID  3 Data type TYPE_TIMESTAMP
    #Unix timestamp of the current time
    def getCurrentTime(self, moduleID):
        guid =  3
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
                
    #Attribute 'Voltage' GUID  4 Data type TYPE_UNSIGNED_NUMBER
    #True RMS Voltage
    def getVoltage(self, moduleID):
        guid =  4
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Frequency' GUID  5 Data type TYPE_UNSIGNED_NUMBER
    #Frequency
    def getFrequency(self, moduleID):
        guid =  5
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Current' GUID  6 Data type TYPE_UNSIGNED_NUMBER
    #Current true RMS
    def getCurrent(self, moduleID, portnumber=1, length=1):
        guid =  6
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Power' GUID  7 Data type TYPE_UNSIGNED_NUMBER
    #Real Power
    def getPower(self, moduleID, portnumber=1, length=1):
        guid =  7
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'StatePortCur' GUID  8 Data type TYPE_ENUM
    #current port state
    def getStatePortCur(self, moduleID, portnumber=1, length=1):
        guid =  8
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'ActiveEnergy' GUID  9 Data type TYPE_UNSIGNED_NUMBER
    #Active Energy
    def getActiveEnergy(self, moduleID, portnumber=1, length=1):
        guid =  9
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'ApparentEnergy' GUID  10 Data type TYPE_UNSIGNED_NUMBER
    #Apparent Energy
    def getApparentEnergy(self, moduleID, portnumber=1, length=1):
        guid =  10
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Temperature' GUID  11 Data type TYPE_SIGNED_NUMBER
    #Temperature
    def getTemperature(self, moduleID):
        guid =  11
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MaxCurrent' GUID  5000 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Maximum port current occurred since last reset
    def getMaxCurrent(self, moduleID, portnumber=1, length=1):
        guid =  5000
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMaxCurrent(self, moduleID, portnumber=1):
        guid =  5000
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, 1)
        return self._parent._getObjectFromData(data, valDef, count=1)
        
    #Attribute 'MaxPower' GUID  5001 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Maximum port power occurred since last reset
    def getMaxPower(self, moduleID, portnumber=1, length=1):
        guid =  5001
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMaxPower(self, moduleID, portnumber=1):
        guid =  5001
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, 1)
        return self._parent._getObjectFromData(data, valDef, count=1)
        
    #Attribute 'MaxTotalCurrent' GUID  5002 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Maximum total current occurred since last reset
    def getMaxTotalCurrent(self, moduleID):
        guid =  5002
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMaxTotalCurrent(self, moduleID):
        guid =  5002
        portnumber=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, 1)
        return self._parent._getObjectFromData(data, valDef, count=1)
        
    #Attribute 'MaxTotalPower' GUID  5003 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Maximum total power occurred since last reset
    def getMaxTotalPower(self, moduleID):
        guid =  5003
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMaxTotalPower(self, moduleID):
        guid =  5003
        portnumber=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, 1)
        return self._parent._getObjectFromData(data, valDef, count=1)
        
    #Attribute 'MaxVoltage' GUID  5004 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Maximum voltage occurred since last reset
    def getMaxVoltage(self, moduleID):
        guid =  5004
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMaxVoltage(self, moduleID):
        guid =  5004
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MinVoltage' GUID  5005 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Minimum voltage occurred since last reset
    def getMinVoltage(self, moduleID):
        guid =  5005
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMinVoltage(self, moduleID):
        guid =  5005
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MinTemperature' GUID  5006 Data type TYPE_SIGNED_NUMBER_WITH_TS
    #Minimum temperature occurred since last reset
    def getMinTemperature(self, moduleID):
        guid =  5006
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMinTemperature(self, moduleID, value):
        guid =  5006
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MaxTemperature' GUID  5007 Data type TYPE_SIGNED_NUMBER_WITH_TS
    #Maximum temperature occurred since last reset
    def getMaxTemperature(self, moduleID):
        guid =  5007
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def resetMaxTemperature(self, moduleID):
        guid =  5007
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Address' GUID  10000 Data type TYPE_UNSIGNED_NUMBER
    #Identification of the module
    def getAddress(self, moduleID, portnumber=1, length=1):
        guid =  10000
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'ModuleName' GUID  10001 Data type TYPE_STRING
    #Module name
    def getModuleName(self, moduleID):
        guid =  10001
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setModuleName(self, moduleID, value):
        guid =  10001
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'FirmwareVersion' GUID  10002 Data type TYPE_VERSION
    #Firmware version
    def getFirmwareVersion(self, moduleID):
        guid =  10002
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'HardwareVersion' GUID  10003 Data type TYPE_VERSION
    #Hardware version
    def getHardwareVersion(self, moduleID):
        guid =  10003
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'FirmwareID' GUID  10004 Data type TYPE_STRING
    #Identification of the firmware
    def getFirmwareID(self, moduleID):
        guid =  10004
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'HardwareID' GUID  10005 Data type TYPE_STRING
    #Identification of the hardware
    def getHardwareID(self, moduleID):
        guid =  10005
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TemperatureUnitSelector' GUID  10010 Data type TYPE_ENUM
    def getTemperatureUnitSelector(self, moduleID):
        guid =  10010
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setTemperatureUnitSelector(self, moduleID, value):
        guid =  10010
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'PortName' GUID  10034 Data type TYPE_STRING
    #Name of the port
    def getPortName(self, moduleID, portnumber=1, length=1):
        guid =  10034
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setPortName(self, moduleID, value, portnumber=1):
        guid =  10034
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'PortState' GUID  10035 Data type TYPE_ENUM
    #The state of the port, only used to set the port state, see current port state to get the port state
    def setPortState(self, moduleID, value, portnumber=1):
        guid =  10035
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'CurrentPriorOff' GUID  10036 Data type TYPE_UNSIGNED_NUMBER
    #Priority level switch off when maximum total current exceeds threshold
    def getCurrentPriorOff(self, moduleID, portnumber=1, length=1):
        guid =  10036
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setCurrentPriorOff(self, moduleID, value, portnumber=1, ):
        guid =  10036
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'DelayOn' GUID  10037 Data type TYPE_UNSIGNED_NUMBER
    #Port activation delay after power recycle
    def getDelayOn(self, moduleID, portnumber=1, length=1):
        guid =  10037
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setDelayOn(self, moduleID, value, portnumber=1, ):
        guid =  10037
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxCurrentOff' GUID  10038 Data type TYPE_UNSIGNED_NUMBER
    #Maximum port current switch off level
    def getMaxCurrentOff(self, moduleID, portnumber=1, length=1):
        guid =  10038
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxCurrentOff(self, moduleID, value, portnumber=1, ):
        guid =  10038
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxCurrentWarning' GUID  10039 Data type TYPE_UNSIGNED_NUMBER
    #Maximum port current warning level
    def getMaxCurrentWarning(self, moduleID, portnumber=1, length=1):
        guid =  10039
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxCurrentWarning(self, moduleID, value, portnumber=1, ):
        guid =  10039
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxPowerOff' GUID  10040 Data type TYPE_UNSIGNED_NUMBER
    #Maximum port power switch off level
    def getMaxPowerOff(self, moduleID, portnumber=1, length=1):
        guid =  10040
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxPowerOff(self, moduleID, value, portnumber=1, ):
        guid =  10040
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxPowerWarning' GUID  10041 Data type TYPE_UNSIGNED_NUMBER
    #Maximum port power warning level
    def getMaxPowerWarning(self, moduleID, portnumber=1, length=1):
        guid =  10041
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxPowerWarning(self, moduleID, value, portnumber=1, ):
        guid =  10041
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxTotalCurrentOff' GUID  10042 Data type TYPE_UNSIGNED_NUMBER
    #Maximum total current switch off level
    def getMaxTotalCurrentOff(self, moduleID):
        guid =  10042
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxTotalCurrentOff(self, moduleID, value):
        guid =  10042
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxTotalCurrentWarning' GUID  10043 Data type TYPE_UNSIGNED_NUMBER
    #Maximum total current warning level
    def getMaxTotalCurrentWarning(self, moduleID):
        guid =  10043
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxTotalCurrentWarning(self, moduleID, value):
        guid =  10043
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxTotalPowerOff' GUID  10044 Data type TYPE_UNSIGNED_NUMBER
    #Maximum total power switch off level
    def getMaxTotalPowerOff(self, moduleID):
        guid =  10044
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxTotalPowerOff(self, moduleID, value):
        guid =  10044
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxTotalPowerWarning' GUID  10045 Data type TYPE_UNSIGNED_NUMBER
    #Maximum total power warning level
    def getMaxTotalPowerWarning(self, moduleID):
        guid =  10045
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxTotalPowerWarning(self, moduleID, value):
        guid =  10045
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxVoltageOff' GUID  10046 Data type TYPE_UNSIGNED_NUMBER
    #Maximum voltage switch off level
    def getMaxVoltageOff(self, moduleID):
        guid =  10046
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxVoltageOff(self, moduleID, value):
        guid =  10046
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxVoltageWarning' GUID  10047 Data type TYPE_UNSIGNED_NUMBER
    #Maximum voltage warning level
    def getMaxVoltageWarning(self, moduleID):
        guid =  10047
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxVoltageWarning(self, moduleID, value):
        guid =  10047
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinVoltageOff' GUID  10048 Data type TYPE_UNSIGNED_NUMBER
    #Minimum voltage switch off level
    def getMinVoltageOff(self, moduleID):
        guid =  10048
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinVoltageOff(self, moduleID, value):
        guid =  10048
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinVoltageWarning' GUID  10049 Data type TYPE_UNSIGNED_NUMBER
    #Minimum voltage warning level
    def getMinVoltageWarning(self, moduleID):
        guid =  10049
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinVoltageWarning(self, moduleID, value):
        guid =  10049
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'ActiveEnergyReset' GUID  10050 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Active Energy
    def setActiveEnergyReset(self, moduleID, value, portnumber=1, ):
        guid =  10050
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'ApparentEnergyReset' GUID  10051 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Apparent Energy
    def setApparentEnergyReset(self, moduleID, value, portnumber=1, ):
        guid =  10051
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinTemperatureWarning' GUID  10052 Data type TYPE_SIGNED_NUMBER
    def getMinTemperatureWarning(self, moduleID):
        guid =  10052
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinTemperatureWarning(self, moduleID, value):
        guid =  10052
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxTemperatureWarning' GUID  10053 Data type TYPE_SIGNED_NUMBER
    def getMaxTemperatureWarning(self, moduleID):
        guid =  10053
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxTemperatureWarning(self, moduleID, value):
        guid =  10053
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'Startuptime' GUID  10066 Data type TYPE_UNSIGNED_NUMBER
    def getStartuptime(self, moduleID):
        guid =  10066
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'JumpBoot' GUID  40000 Data type TYPE_COMMAND
    #Enter bootloader mode. Normally this command is only sent to application program. When the bootloader is already running, this command will only reply a positive acknowledge.
    def getJumpBoot(self, moduleID):
        guid =  40000
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setJumpBoot(self, moduleID, value):
        guid =  40000
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'GotoFactoryMode' GUID  40002 Data type TYPE_COMMAND
    def setGotoFactoryMode(self, moduleID, value):
        guid =  40002
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
                     
    #Attribute 'ApparentPower' GUID  15 Data type TYPE_UNSIGNED_NUMBER
    #Apparent power (this is the product of the current and the voltage)
    def getApparentPower(self, moduleID, portnumber=1, length=1):
        guid =  15
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'ModInfo' GUID  40008 Data type TYPE_COMMAND
    def getModInfo(self, moduleID):
        guid =  40008
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Monitor' GUID  50000 Data type TYPE_POINTER
    #Get the monitor values
    def getMonitor(self, moduleID):
        guid =  50000
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Parameter' GUID  50001 Data type TYPE_POINTER
    #get all parameters
    def getParameter(self, moduleID):
        guid =  50001
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'VoltageTimeSamples' GUID  50004 Data type TYPE_RAW
    #Get the voltage samples in oscilloscope view mode
    def getVoltageTimeSamples(self, moduleID, portnumber=1, length=1):
        guid =  50004
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'CurrentTimeSamples' GUID  50005 Data type TYPE_RAW
    #Get the current samples in oscilloscope view mode
    def getCurrentTimeSamples(self, moduleID, portnumber=1, length=1):
        guid =  50005
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'VoltageFreqSamples' GUID  50006 Data type TYPE_RAW
    #Get the frequency analyse of the voltage
    def getVoltageFreqSamples(self, moduleID, portnumber=1, length=1):
        guid =  50006
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'CurrentFreqSamples' GUID  50007 Data type TYPE_RAW
    #Get the frequency analyse of the current
    def getCurrentFreqSamples(self, moduleID, portnumber=1, length=1):
        guid =  50007
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'Eeprom' GUID  50008 Data type TYPE_RAW
    #Attribute 'CallibrationValues' GUID  50009 Data type TYPE_RAW
    def getCallibrationValues(self, moduleID, portnumber=1, length=1):
        guid =  50009
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'PowerFactor' GUID  16 Data type TYPE_UNSIGNED_NUMBER
    #Powerfactor 
    def getPowerFactor(self, moduleID, portnumber=1, length=1):
        guid =  16
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MinCurrent' GUID  5010 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Minimum port current occurred since last reset
    def getMinCurrent(self, moduleID, portnumber=1, length=1):
        guid =  5010
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinCurrent(self, moduleID, value, portnumber=1, ):
        guid =  5010
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinPower' GUID  5011 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Minimum port power occured since last reset
    def getMinPower(self, moduleID, portnumber=1, length=1):
        guid =  5011
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinPower(self, moduleID, value, portnumber=1, ):
        guid =  5011
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinPowerFactor' GUID  5012 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Minimum powerfactor occured per port since last reset
    def getMinPowerFactor(self, moduleID, portnumber=1, length=1):
        guid =  5012
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinPowerFactor(self, moduleID, value, portnumber=1, ):
        guid =  5012
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxPowerFactor' GUID  5013 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Maximum powerfactor occured per port since last reset
    def getMaxPowerFactor(self, moduleID, portnumber=1, length=1):
        guid =  5013
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxPowerFactor(self, moduleID, value, portnumber=1, ):
        guid =  5013
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'BootJumpApp' GUID  60001 Data type TYPE_COMMAND
    #Jump to the application, which starts at 0x4000.  
    def setBootJumpApp(self, moduleID, value):
        guid =  60001
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'TotalCurrent' GUID  17 Data type TYPE_UNSIGNED_NUMBER
    #Total current
    def getTotalCurrent(self, moduleID):
        guid =  17
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TotalRealPower' GUID  18 Data type TYPE_UNSIGNED_NUMBER
    #Total real power
    def getTotalRealPower(self, moduleID):
        guid =  18
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TotalApparentPower' GUID  19 Data type TYPE_UNSIGNED_NUMBER
    #Total apparent power
    def getTotalApparentPower(self, moduleID):
        guid =  19
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TotalActiveEnergy' GUID  20 Data type TYPE_UNSIGNED_NUMBER
    #Total active energy
    def getTotalActiveEnergy(self, moduleID):
        guid =  20
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TotalApparentEnergy' GUID  21 Data type TYPE_UNSIGNED_NUMBER
    #Total apparent energy
    def getTotalApparentEnergy(self, moduleID):
        guid =  21
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'TotalPowerFactor' GUID  22 Data type TYPE_UNSIGNED_NUMBER
    #Total power factor
    def getTotalPowerFactor(self, moduleID):
        guid =  22
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'MinTotalCurrent' GUID  5014 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Minimum port current occurred since last reset
    def getMinTotalCurrent(self, moduleID):
        guid =  5014
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinTotalCurrent(self, moduleID, value):
        guid =  5014
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinTotalPower' GUID  5015 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Minimum port power occurred since last reset
    def getMinTotalPower(self, moduleID):
        guid =  5015
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinTotalPower(self, moduleID, value):
        guid =  5015
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MinTotalPowerFactor' GUID  5016 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Minimum total power factor occurred since last reset
    def getMinTotalPowerFactor(self, moduleID):
        guid =  5016
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMinTotalPowerFactor(self, moduleID, value):
        guid =  5016
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MaxTotalPowerFactor' GUID  5017 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Maximum total power factor occurred since last reset
    def getMaxTotalPowerFactor(self, moduleID):
        guid =  5017
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    def setMaxTotalPowerFactor(self, moduleID, value):
        guid =  5017
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'ActiveTotalEnergyReset' GUID  10071 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Active Total Energy / time of reset + value at that time        
    def setActiveTotalEnergyReset(self, moduleID, value):
        guid =  10071
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'ApparentTotalEnergyReset' GUID  10072 Data type TYPE_UNSIGNED_NUMBER_WITH_TS
    #Apparent Total Energy / time of reset + value at that time        
    def setApparentTotalEnergyReset(self, moduleID, value):
        guid =  10072
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'MonitorAutoRefresh' GUID  50010 Data type TYPE_POINTER
    #Get the monitor values from the module that are auto refreshed
    def getMonitorAutoRefresh(self, moduleID):
        guid =  50010
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.getAttribute(moduleID, guid, portnumber, length)
        return self._parent._getObjectFromData(data, valDef, count=length)
        
    #Attribute 'DoHotReset' GUID  40014 Data type TYPE_COMMAND
    #Hot reset of the device
    def setDoHotReset(self, moduleID, value):
        guid =  40014
        portnumber=1
        length=1
        valDef = self._parent._guidTable[guid]
        data = self._parent._client.setAttribute(moduleID, guid, convert.value2bin(value, valDef),portnumber)
        return self._parent._getObjectFromData(data, valDef, setter=True)
        
    #Attribute 'EventQueue' GUID  50011 Data type TYPE_RAW
    #The pointers!!
#    def getPower(self, moduleID):
#        guid =  7
#        paramInfo = [
#        (self._parent._guidTable[1],1),
#        (self._parent._guidTable[2],1),
#        (self._parent._guidTable[3],1),
#        (self._parent._guidTable[4],1),
#        (self._parent._guidTable[5],1),
#        (self._parent._guidTable[6],8),
#        (self._parent._guidTable[7],8),
#        (self._parent._guidTable[8],8),
#        (self._parent._guidTable[9],8),
#        (self._parent._guidTable[10],8),
#        (self._parent._guidTable[11],1),
#        (self._parent._guidTable[5000],8),
#        (self._parent._guidTable[5001],8),
#        (self._parent._guidTable[5002],1),
#        (self._parent._guidTable[5003],1),
#        (self._parent._guidTable[5004],1),
#        (self._parent._guidTable[5005],1),
#        (self._parent._guidTable[5006],1),
#        (self._parent._guidTable[5007],1),
#        (self._parent._guidTable[10000],2),
#        (self._parent._guidTable[10001],1),
#        (self._parent._guidTable[10002],1),
#        (self._parent._guidTable[10003],1),
#        (self._parent._guidTable[10004],1),
#        (self._parent._guidTable[10005],1),
#        (self._parent._guidTable[10010],1),
#        (self._parent._guidTable[10034],8),
#        (self._parent._guidTable[10035],8),
#        (self._parent._guidTable[10036],8),
#        (self._parent._guidTable[10037],8),
#        (self._parent._guidTable[10038],8),
#        (self._parent._guidTable[10039],8),
#        (self._parent._guidTable[10040],8),
#        (self._parent._guidTable[10041],8),
#        (self._parent._guidTable[10042],1),
#        (self._parent._guidTable[10043],1),
#        (self._parent._guidTable[10044],1),
#        (self._parent._guidTable[10045],1),
#        (self._parent._guidTable[10046],1),
#        (self._parent._guidTable[10047],1),
#        (self._parent._guidTable[10048],1),
#        (self._parent._guidTable[10049],1),
#        (self._parent._guidTable[10050],8),
#        (self._parent._guidTable[10051],8),
#        (self._parent._guidTable[10052],1),
#        (self._parent._guidTable[10053],1),
#        (self._parent._guidTable[10066],1),
#        (self._parent._guidTable[40000],1),
#        (self._parent._guidTable[40001],1),
#        (self._parent._guidTable[40002],1),
#        (self._parent._guidTable[40003],1),
#        (self._parent._guidTable[40004],1),
#        (self._parent._guidTable[40005],1),
#        (self._parent._guidTable[40006],1),
#        (self._parent._guidTable[15],8),
#        (self._parent._guidTable[40008],1),
#        (self._parent._guidTable[50000],0),
#        (self._parent._guidTable[50001],0),
#        (self._parent._guidTable[50004],256),
#        (self._parent._guidTable[50005],256),
#        (self._parent._guidTable[50006],256),
#        (self._parent._guidTable[50007],256),
#        (self._parent._guidTable[50008],0),
#        (self._parent._guidTable[50009],256),
#        (self._parent._guidTable[16],8),
#        (self._parent._guidTable[5010],8),
#        (self._parent._guidTable[5011],8),
#        (self._parent._guidTable[5012],8),
#        (self._parent._guidTable[5013],8),
#        (self._parent._guidTable[60001],1),
#        (self._parent._guidTable[17],1),
#        (self._parent._guidTable[18],1),
#        (self._parent._guidTable[19],1),
#        (self._parent._guidTable[20],1),
#        (self._parent._guidTable[21],1),
#        (self._parent._guidTable[22],1),
#        (self._parent._guidTable[5014],1),
#        (self._parent._guidTable[5015],1),
#        (self._parent._guidTable[5016],1),
#        (self._parent._guidTable[5017],1),
#        (self._parent._guidTable[10071],1),
#        (self._parent._guidTable[10072],1),
#        (self._parent._guidTable[50010],0),
#        (self._parent._guidTable[40014],1),
#        (self._parent._guidTable[50011],32),
#        ]
      
        #Get pointer's data
#        data = self._parent._client.getAttribute(moduleID, guid)
#        return convert.pointer2values(data, paramInfo)
