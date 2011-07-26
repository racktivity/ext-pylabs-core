import httplib
from pylabs import q
import ecsclient

client = None

def getClient():
    global client
    return client


def setup():
    global client
    config = q.config.getConfig("scenarioparams")['main']
    ecsaddress = config['ecsaddress']
    ecsport = config.get("ecsport", 8111)
    ecslogin = config['ecslogin']
    ecspassword = config['ecspassword']
    
    client = ecsclient.ECSClient(ecsaddress, ecsport, ecslogin, ecspassword)


def teardown():
    pass
