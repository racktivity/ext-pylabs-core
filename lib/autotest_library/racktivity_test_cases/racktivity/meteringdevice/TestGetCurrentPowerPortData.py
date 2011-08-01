from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid, getEmulatorConfig

EMPTY_GUID = '00000000-0000-0000-0000-000000000000'
METERINGDEVICE_NAME = 'test-racktivitydevice'
IPADDRESS_NAME = 'test-localip'

mdguid = pmguid = ipaddress = None

def getCloudapi():
    return p.api.action.racktivity

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def getPowerModuleGuid():
    global pmguid
    return pmguid

def getIPAddress():
    global ipaddress
    return ipaddress

def setup():
    global mdguid, pmguid, ipaddress
    ipaddress, port, type = getEmulatorConfig()
    mdguid, pmguid = racktivity_test_library.meteringdevice.createRacktivity(METERINGDEVICE_NAME, getRackGuid(),
                                                                   ipaddress=ipaddress,
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
    


