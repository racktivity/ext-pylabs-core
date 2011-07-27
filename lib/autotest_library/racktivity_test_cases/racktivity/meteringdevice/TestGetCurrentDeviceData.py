from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid, getEmulatorConfig

EMPTY_GUID = '00000000-0000-0000-0000-000000000000'
METERINGDEVICE_NAME = 'test-racktivitydevice'
IPADDRESS_NAME = 'test-localip'
mdguid = pmguid = ipaddressguid = None

def getCloudapi():
    return p.api.action.racktivity

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def getPowerModuleGuid():
    global pmguid
    return pmguid

def getIPAddressGuid():
    global ipaddressguid
    return ipaddressguid

def setup():
    global mdguid, pmguid, ipaddressguid
    ip,port,type = getEmulatorConfig()
    ipaddressguid = racktivity_test_library.ipaddress.create(IPADDRESS_NAME, ip)
    mdguid, pmguid = racktivity_test_library.meteringdevice.createRacktivity(METERINGDEVICE_NAME, getRackGuid(),
                                                                   ipaddressguid=ipaddressguid,
                                                                   meteringdevicetype=type,
                                                                   port=port)
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())

def testGetCurrentDeviceDataAll_1():
    """
    @description: [0.16.06.01] Test Get current device data
    @id: 0.16.06.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.getCurrentDeviceData(guid, 'all')
    @expected_result: All the metering device data are found
    """
    cloudapi = getCloudapi()
    result = cloudapi.meteringdevice.getCurrentDeviceData(getMeteringdeviceGuid(), "all")['result']
    assert_true(result['returncode'], "Return code is False")
    values = result['value']
    
    #check voltage
    assert_true('Voltage' in values, "Voltage data doesn't exist")
    assert_true(isinstance(values['Voltage'], float), "Voltage is not float")
    
    #check Ports data
    assert_true('Ports' in values, "Ports data doesn't exist")
