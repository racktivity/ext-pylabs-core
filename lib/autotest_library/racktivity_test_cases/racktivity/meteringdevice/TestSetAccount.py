from nose.tools import *
from cloud_api_client.Exceptions import CloudApiException
import racktivity_test_library
from pymonkey import i, q
from . import getRackGuid, getEmulatorConfig
import nose.plugins.skip

DEVICE_NAME = 'test-meteringdevice'
LOGIN = 'mynewuser'
PASSWORD = 'mynewpassword'
IPADDRESS_NAME = 'test-localip'

OLD_LOGIN = "root"
OLD_PASSWORD = "rooter"
SUPPORTED_DEVICES = ["racktivity"]

mdguid = ipaddressguid = None

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def getIPAddressGuid():
    global ipaddressguid
    return ipaddressguid

def setup():
    global mdguid, ipaddressguid
    ip,port,type = getEmulatorConfig()
    if type not in SUPPORTED_DEVICES:
        raise nose.plugins.skip.SkipTest("Type %s doesn't support setAccount function"%type)
    ipaddressguid = racktivity_test_library.ipaddress.create(IPADDRESS_NAME, ip)
    mdguid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid(), ipaddressguid=ipaddressguid, port=port, meteringdevicetype=type)

def teardown():
    #reset the username and password to the original values.
    cloudapi = getCloudapi()
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testSetAccount_1():
    """
    @description: [0.16.16.01] Test Set Account on a device
    @id: 0.16.16.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.setAccount(guid, login, password)
    @expected_result: an/ access account is added to the metering device
    """
    ip,port,type = getEmulatorConfig()
    cloudapi = getCloudapi()
    originalAccount = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid()).accounts[0]
    cloudapi.meteringdevice.setAccount(getMeteringdeviceGuid(), LOGIN, PASSWORD, "admin")
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    account = md.accounts[0]
    
    assert_equal(account.login, LOGIN)
    assert_equal(account.password, PASSWORD)
    
    #make sure that the device username/password has been really changed.
    q.clients.racktivitycontroller.connect(ip, port, LOGIN, PASSWORD)
    #Revert username/password back to its original values 
    cloudapi.meteringdevice.setAccount(getMeteringdeviceGuid(), originalAccount.login, originalAccount.password, "admin")
