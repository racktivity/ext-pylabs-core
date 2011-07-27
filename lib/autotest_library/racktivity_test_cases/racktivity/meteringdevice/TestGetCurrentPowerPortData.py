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
    return i.config.cloudApiConnection.find('main')

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
    
def testGetCurrentPowerPortData_1():
    """
    @description: [0.16.07.01] Test Get current power port data
    @id: 0.16.07.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.getCurrentPowerPortData(guid, label, 'Current')
    @expected_result: the data for the given power port is returned
    """
    cloudapi = getCloudapi()
    result = cloudapi.meteringdevice.getCurrentPowerPortData(getPowerModuleGuid(), 'output-1', "Current")['result']
    assert_true(result['returncode'], "Return code is False")
    value = result['value']
    
    #check current
    assert_true(isinstance(value, float), "Current is not float")

def testGetCurrentPowerPortData_2():
    """
    @description: [0.16.07.02] Test Get current power port data with wrong metering type
    @id: 0.16.07.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.getCurrentPowerPortData(guid, label, 'Temperature')
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.meteringdevice.getCurrentPowerPortData, getPowerModuleGuid(), 'output-1', "Temperature")
    


