# This module contains special functions to calculate/validate attributes that return calculated values
# all functions has the following signature calc<attrName>(rs, module, id, expRes):
# rs is ractivity object, module is the module name ("power","master",..)
# id is the module id ("P1","T1",...)
# expRes is the expected return result from the main script
# return True, result (to let the main script compare your result with the expected one)
# return False, None if you want to customize the error message or have different check criteria (i.e < or > instead of =) 
import time
import sys

#This function will compare two array of values (expected vs actual) using op operation
#Return False if it failed to compare  
def compareTwoArrays(arrVal, op, arrExp, msg):
    l1 = len(arrVal)
    l2 = len(arrExp)
    success=True
    if l1 != l2:
        print "compareTwoArrays got two arrays of different size %d %d\n", (l1,l2)
        return False
    for i in xrange(0, l1):
        if eval("%s %s %s"%(arrVal[i],op, arrExp[i])):
            sys.stderr.write(msg%(i+1, repr(arrVal[i]), repr(arrExp[i])) + "\n")
            success = False
    return success

def calcPower(rs, module, id, expRes):
    #Wait a little bit for the emulator to refresh
    mod = getattr(rs, module)
    expLen = len(expRes)
    currentValues = mod.getCurrent(id, length=expLen)[1]
    volatgeValue = mod.getVoltage(id)[1]
    powerValues = [ c * volatgeValue for c in currentValues]
    #powerValues = [ c * v for c,v in zip(currentValues,volatgeValues)]
    return compareTwoArrays(powerValues,"!=", expRes, "Error: in calcPower port %d should have value %s not %s")

def calcStatePortCur(rs, module, id, expRes):
    mod = getattr(rs, module)
    values = mod.getStatePortCur(id, length=len(expRes))[1]
    return compareTwoArrays(values, "!=", expRes, "Error: in calcStatePortCur value of port %d is %s expected %s")

def calcMaxCurrent(rs, module, id, expRes):
    #time.sleep(1) #Delay to give the emulator chance to detect changes in Current
    mod = getattr(rs, module)
    values = mod.getCurrent(id, length=len(expRes))[1]
    #MaxCurrent is not float, so current also should be converted to int first
    for i in xrange(0,len(values)):
        values[i] = int(values[i])
    return compareTwoArrays(values, ">", expRes, "Error: in calcMaxCurrent port %d has Current (%s) > MaxCurrent (%s)")

def calcMaxVoltage(rs, module, id, expRes):
    mod = getattr(rs, module)
    voltage = mod.getVoltage(id)[1]
    if expRes[0] < voltage:
        sys.stderr.write("Error: Voltage (%s) > MaxVoltage (%s)\n"%(repr(voltage), repr(expRes[0])))
        return False
    return True

def calcMinVoltage(rs, module, id, expRes):
    mod = getattr(rs, module)
    voltage = mod.getVoltage(id)[1]
    if expRes[0] > voltage:
        sys.stderr.write("Error: Voltage (%s) < MinVoltage (%s)\n"%(repr(voltage), repr(expRes)))
        return False
    return True

def calcMaxTotalCurrent(rs, module, id, expRes):
    mod = getattr(rs, module)
    values = mod.getMaxCurrent(id, length=8)[1]
    maxTotal = sum(values)
    if maxTotal != expRes[0]:
        sys.stderr.write("Error:in calcMaxTotalCurrent, MaxTotalCurrent is %s but sum(getMaxCurrent) is %s\n"%(expRes[0], maxTotal))
        return False
    return True

def calcMaxPower(rs, module, id, expRes):
    mod = getattr(rs, module)
    values = mod.getPower(id, length=len(expRes))[1]
    return compareTwoArrays(values, ">", expRes, "Error: in calcMaxPower port %d has power (%s) > MaxPower (%s)")

def calcMaxTotalPower(rs, module, id, expRes):
    mod = getattr(rs, module)
    res = mod.getMaxPower(id, length=8)
    maxTotal = sum(res[1])
    if maxTotal != expRes[0]:
        sys.stderr.write("Error:in calcMaxTotalPower, MaxTotalPower is %s but sum(MaxPower) is %s\n"%(expRes[0], maxTotal))
        return False
    return True

def calcLogin(rs, module, id, expRes):
    #That simply means, SKIP this attribute
    return True

def calcCurrent(rs, module, id, expRes):
    time.sleep(10)
    sys.stdout.write("    *Sleep ")
    for i in xrange(0,15):
        time.sleep(0.2)
        sys.stdout.write("z")
        sys.stdout.flush()
    sys.stdout.write("\n")
    mod = getattr(rs, module)
    resLen = len(expRes)
    values = mod.getCurrent(id, length=resLen)[1]
    max = mod.getMaxCurrentOff(id, length=resLen)[1]
    portState = mod.getStatePortCur(id, length=resLen)[1]
    
    for i in xrange(0,resLen):
        if expRes[i] >= max or portState[i] == False:
            expRes[i] = 0             
    return compareTwoArrays(values, "!=", expRes, "Error: Current of port %d returned %s expected %s")   
    
#Read/Write Attributes
def readPortState(rs, module, id, length):
    mod = getattr(rs, module)
    res = rs.power.getStatePortCur(id, length=length)
    if res[0]:
        sys.stderr.write("Error: rs.power.getStatePortCur(%s, length=%s) Failed with code %s\n"%(id, length, res[0]))
        return None
    return res[1]
    
def writeLogin(rs, module, id, data = None):
    return None

def writePassword(rs, module, id, data = None):
    return None
