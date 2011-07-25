import racktivity.sal.client
from racktivity.common.GUIDLoader import Value
import sqlite3
import sys
import os
import random
import math
import getpass
import binascii
import SpecialAttributes
import time
#import AttributeDBIO

EMUDIR="/opt/qbase3/var/racktivity/"
if len(sys.argv) < 3 or sys.argv[1].startswith("-") or sys.argv[2].find(":") <= 0:
    print "Usage: %s <cache file> <hostname:port> [username [password]]"%sys.argv[0]
    sys.exit(1)

#Dictionary hold bad values and expected error code
badValuesDictionary = {
    "number": [(10000000, 12)]
}

#module is "power" or "master", name is "Attribute name"
def buildAttributeCall(module,name,id = "M1", type="get", index = 1, length = 1, data = None):
    func = "rs.%s.%s%s("%(module,type, name)
    if id != "M1":
        func += repr(id) + ","
    if data != None:
        func += repr(data) + ","
    if index > 1:
        func += str(index) + ","
    if length > 1:
        func += "length=%d"%length
    return func + ")"


def giveMeTestValue(vd, default):
    if vd.type == "number":
        #Verify the guid table
        if  vd.max > (2 ** (vd.size * 8)):
            sys.stderr.write("Error in the guid table, %s is bigger than the maximum size\n"%vd.max)
            return None
        val = random.randrange(vd.min,vd.max)
        if vd.scale:
            return float(val) / 10 ** vd.scale
        else:
            return val
    elif vd.type == "IP":
        val = str(random.randrange(0,255))
        for i in xrange(0,3):
            val += ".%d"%random.randrange(0,255) 
        return val
    elif vd.type == "mac":
        val = "%02x"%random.randrange(0,255)
        for i in xrange(0,5):
            val += ":%02x"%random.randrange(0,255) 
        return val
    elif vd.type == "string":
        val = ""
        for i in range(0, vd.length):
            val += chr(random.randrange(0,128))
        #If there is zero in the string trim it
        if val.find("\0") >= 0:
            val = val[0:val.index("\0")]
        return val
    elif vd.type == "bool":
        return random.randrange(0,1) == 1
    elif vd.type == "version":
        val = random.randrange(0,99) / 10.0
        return val
    elif vd.type == "raw":
        r = ""
        for i in xrange(0, vd.size):
            r += chr(random.randrange(0,128))
        return r
    else:
        sys.stderr.write("Warning: type %s is not supported\n"%vd.type)
        return default

def readAttribute(miname,name,module,count, read, valDef):
    if "read" + name in dir(SpecialAttributes):
        func = getattr(SpecialAttributes, "read" + name)
        readResult = func(rs, module, miname, count)
    elif read:
        try:
            func = buildAttributeCall(module,name, miname, "get", length=count)
            result=eval(func)
        except Exception as e:
            sys.stderr.write("Error:%s has caused an exception %s\n"%(func,e))
            return False,None
        if result[0]:
            sys.stderr.write("Error: %s returned error code %d\n"%(func, result[0]))
            return False, None
        readResult = result[1]
    else:
        import AttributeDBIO
        readResult = AttributeDBIO.getAttribute(miname, name, module, count > 1)
        if readResult == None:
            print "        *Warning: no way to read Attribute " + name
            return False, None
        if valDef.type == "raw":
            for i in xrange(0,len(readResult)):
                readResult[i] = readResult[i].ljust(valDef.size, "\0")
        if count == 1:
            readResult = readResult[0]
        
    if count > 1 and not isinstance(readResult,list):
            sys.stderr.write("Error: %s failed, expected value of type List where length=%d\n"%(func,count))
            return False, None
    if isinstance(readResult,list):
        if count == 1:
            sys.stderr.write("Error: %s failed, returned list of values while length=1\n"%func)
            return False, None
        if len(readResult) != count:
            sys.stderr.write("Error: %s failed, returned unexpected number of elements\n"%func)
            return False, None
    return True, readResult


#Return SUCESS(True/False), written value
#If Result = True and written values = None, This attribute will be considered calculated attribute
def writeAttribute(miname,name,module, data, index, write, multiValue):
    #1. If I have write function, I should use it
    if "write" + name in dir(SpecialAttributes):
        func = getattr(SpecialAttributes, "write" + name)
        try:
            value = func(rs, module, miname, data)
        except Exception as e:
            sys.stderr.write("Exception:write%s function says %s\n"%(name,e))
            return False,None
        return True, value
    #2. If the variable is writable I should try to write using the setter
    elif write:
        func = buildAttributeCall(module,name, miname, "set", index, 1, data) 
        try:
            value=eval(func)
            if value:
                sys.stderr.write("Error:%s returned error code %d\n"%(func, value))
                return False, None
        except Exception as e:
            sys.stderr.write("Exception:%s function says %s\n"%(func, e))
            return False,None
        return True, data
    else:
        try:
            import AttributeDBIO
            AttributeDBIO.setAttribute(miname, name, module, data, index, multiValue)
        except Exception as e:
            sys.stderr.write("Exception:Couldn't write value '%s', error was %s\n"%(data, e))
            return False,None
        return True, data
    #4. let the main script try to calculate the function
        return True, None
    
def readPointerAttribute(miname,name,module):
    func =  buildAttributeCall(module,name, miname)
    try:
        result=eval(func)
    except:
        sys.stderr.write("Error:%s has caused an exception\n"%func)
        return None
    #1. Check error code
    if result[0]:
        return result[0]
    
    result = result[1]
    #2. Make sure the result is list
    if not isinstance(result,list):
        sys.stderr.write("Error: (pointer type) %s should return value of type list\n"%func)
        return None
    #3. Get list of expected Data through getters
    vList = []
    for (sName,sCount, sRawValDef, sRead) in con.execute('select g.name,m.count, g.valDef, g.read from modules as m, tbl_guid g where g.guid = m.guid and m.type = ? and m.name=? order by id', (module, name)):
        vDef = Value(sRawValDef)
        if vDef.type == "pointer":
            r = None
        else:
            stat, r = readAttribute(miname, sName, module,sCount, sRead, vDef)
            if not stat:
                sys.stderr.write("Error: getting %s failed, Pointer %s will be skipped \n"%(sName, name))
                return
            r = (r, sName)
        vList.append(r)
    #4. Check the two lengths
    if len(vList) != len(result):
        sys.stderr.write("Error: %s returned %d items, expected %d\n"%(sName, len(result), len(vList)))
        return None
    #4. Compare the result list with the list i have
    for i in xrange(0, len(result)):
        if vList[i] and vList[i][0] != result[i]:
            sys.stderr.write("Error: %s returned invalid result, value of attribute %s should be %s not %s\n"
                             %(func,vList[i][1],repr(result[i]), repr(vList[i][0])))
    return True

print "* Connecting to the database"
db = sys.argv[1]
con = sqlite3.connect(db)
random.seed()

print "* Creating RacSal object"
#should I get user name/password from user or from params?
if len(sys.argv) > 3:
    username = sys.argv[3]
else:
    username = raw_input("Username: ")

if len(sys.argv) > 4:
    password = sys.argv[4]
else:
    password = getpass.getpass("Password: ")
print "Using %s and %s"% (repr(username), repr(password))
host,port = sys.argv[2].split(":")
rs = racktivity.sal.client.RackSal(username.strip(),password.strip(),host,int(port))
for itr in xrange(0,20):
    print "############ Test number %d ###############"%(itr + 1)
    #Set all ports to True
    print "Resetting ports"
    for i in range(0,8):
        rs.power.setPortState("P1",True,i + 1)
    print "Done"
    #Continue
    for (module,) in con.execute("select distinct type from modules"):
        module = str(module)
        miname = module[0].upper() + '1' #Module Instance Name
        print "    *Checking %s Module"%module
        for (guid, name, valDefRaw, read, write, count) in con.execute('select tbl_guid.*,modules.count from tbl_guid,modules where modules.guid = tbl_guid.guid and modules.type="%s"'% module):
            #Skip login and password functions
            if read == write == 0:
                print "        *%s was skipped (No setters nor getters)"%name
                continue
            #Initialize some variables
            readResult = None
            valDef = Value(valDefRaw)
            values = []
            #If pointer Give it to its function
            if valDef.type == "pointer":
                readPointerAttribute(miname,name,module)
                continue
            #Prepare test values
            for i in xrange(0, count):
                values.append(giveMeTestValue(valDef, None))
            #1. Write bad data
                    
            #2. Write good data to all ports
            for i in xrange(0, count):
                stat, value = writeAttribute(miname,name,module, values[i], i + 1, write, count > 1)
                if not stat or value == None:
                    values = None
                    break
                values[i] = value #update this to reflect the actual written data
            if not stat: continue        
            #3. Read data
            stat, returnedValues = readAttribute(miname,name,module,count, read, valDef)
            if not stat:
                continue
            if returnedValues != None:
                if count == 1: returnedValues = [returnedValues]
                #4. Compare
                if ("calc" + name in dir(SpecialAttributes)):
                    #If there is a function to calc this field let it handle the whole thing
                    func = getattr(SpecialAttributes, "calc" + name)
                    #This func take the expected result along with other info to decide weather the value is correct or not
                    #if the value is not correct the function can decide to let this script taking care of the error message (handle=true)
                    #Or if the function wants to print custom error message then handle should be false
                    #for i in xrange(0, count):
                    try:
                        result = func(rs,module,miname,returnedValues)
                    except Exception as e:
                        sys.stderr.write("Error while calculating %s exception was : %s"%(name, e))
                        break
                    if not result:
                        continue
                elif read and values: #If This attribute was readable and I have values to compare
                    for i in xrange(0, count):
                        if values[i] != returnedValues[i]:
                            if valDef.type == "raw":
                                sys.stderr.write(name + " Failed: expected '" + values[i] + "' got '" + returnedValues[i] + "'\n")
                            else:
                                sys.stderr.write(name + " Failed: expected " + repr(values[i]) + " got " + repr(returnedValues[i]) + "\n")
print "Done"
