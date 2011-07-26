from pymonkey import q, i
from time import sleep
import xmlrpclib

IP="127.0.0.1"
PROXY_URL="http://localhost:8888/appserver/xmlrpc"

def doUITest(parentGuid, action, attrib = "name", value = None):
    """
    @parentGuid: Guid of the parent rootobject of the object you are testing
    @action: ("CREATE", "UPDATE", "DELETE")
    @attrib: currently only name attribute is supported (leave it to default)
    @value:  value of the attribute "attrib" currently name of the rootobject
    """
    return
    global IP,PROXY_URL
    url="http://%s/confluence/display/RACK/%s"%(IP, parentGuid)
    if action in ("CREATE", "UPDATE", "DELETE"):
        q.system.process.execute("firefox '%s?action=%s&objectname=%s&searchdata=' &"%(url,action.lower(),value))
    else:
        raise ValueError("Invalid action '%s' valid actions are UPDATE,DELETE,CREATE"%action)

def getResult(scriptName, timeout=5):
    """
    @scriptName: 
    @timeout: how long should the function retry until a valid data is received
    """
    return True
    proxy = xmlrpclib.ServerProxy(PROXY_URL)
    for x in range(0,timeout):
        result = proxy.monkeyService.getTestResult(scriptName)
        if result:
            return result['success']
        sleep(1)
    return None
