from nose.tools import *
from cloud_api_client.Exceptions import CloudApiException
import racktivity_test_library
from pymonkey import i, q
from . import getRackGuid, getEmulatorConfig

EMPTY_GUID = '00000000-0000-0000-0000-000000000000'
METERINGDEVICE_NAME = 'test-racktivitydevice'
IPADDRESS_NAME = 'test-localip'
PORT_LABEL = 'output-1'
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
    
def testPowerOnOffPowerPort_1():
    """
    @description: [0.16.14.01] Test Power On/Off Power Port
    @id: 0.16.14.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.powerOffPowerPort(guid, label)
             cloudapi.meteringdevice.powerOnPowerPort(guid, label)
    @expected_result: The port status is set to ON then OFF
              
    """
    cloudapi = getCloudapi()
    
    oldstatus = None
    status = None
    status = cloudapi.meteringdevice.getPowerPortStatus(getPowerModuleGuid(), PORT_LABEL)['result']['status']
    if status:
        cloudapi.meteringdevice.powerOffPowerPort(getPowerModuleGuid(), PORT_LABEL)
    else:
        cloudapi.meteringdevice.powerOnPowerPort(getPowerModuleGuid(), PORT_LABEL)

    oldStatus = cloudapi.meteringdevice.getPowerPortStatus(getPowerModuleGuid(), PORT_LABEL)['result']['status']
    assert_not_equal(status, oldstatus, "Port status didn't change")

def testPowerOnOffPowerPort_2():
    """
    @description: [0.16.14.02] Test Power On/Off Power Port with wrong port label
    @id: 0.16.14.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.powerOffPowerPort(guid, wronglabel)
             cloudapi.meteringdevice.powerOnPowerPort(guid, wronglabel)
    @expected_result: Power ON/OFF action should fail because of wrong port label
              
    """
    cloudapi = getCloudapi()
    assert_raises(CloudApiException, cloudapi.meteringdevice.powerOnPowerPort, getPowerModuleGuid(), 'output-111')
    assert_raises(CloudApiException, cloudapi.meteringdevice.powerOffPowerPort, getPowerModuleGuid(), 'output-111')
    


