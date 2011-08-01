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
    ip,port,type = getEmulatorConfig()
    mdguid, pmguid = racktivity_test_library.meteringdevice.createRacktivity(METERINGDEVICE_NAME, getRackGuid(),
                                                                   ipaddress=ipaddress,
                                                                   meteringdevicetype=type,
                                                                   port=port)

def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testGetPowerPortStatus_1():
    """
    @description: [0.16.08.01] Test Get power port status
    @id: 0.16.08.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.getPowerPortStatus(guid, label)
    @expected_result: Power port status is returned
    """
    cloudapi = getCloudapi()
    result = cloudapi.meteringdevice.getPowerPortStatus(getPowerModuleGuid(), 'output-1')['result']
    assert_true(result['returncode'], "Return code is False")
    
    value = result['status']
    #check current
    assert_true(isinstance(value, bool), "Current is not float")
    if value:
        assert_equal(result['text'], 'On', "Port is on but text representation is '%s'" % result['text'])
    else:
        assert_equal(result['text'], 'Off', "Port is off but text representation is '%s'" % result['text'])

def testGetCurrentPowerPortData_2():
    """
    @description: [0.16.08.02] Test Get power port status with wrong port label
    @id: 0.16.08.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.getPowerPortStatus(guid, wronglabel)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.meteringdevice.getPowerPortStatus, getPowerModuleGuid(), 'output-111')
    


