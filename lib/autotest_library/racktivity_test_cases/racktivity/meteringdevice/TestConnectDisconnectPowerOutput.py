from nose.tools import *
from cloud_api_client.Exceptions import CloudApiException
import racktivity_test_library
from pymonkey import i, q
from . import getRackGuid

EMPTY_GUID = '00000000-0000-0000-0000-000000000000'
METERINGDEVICE_NAME = 'test-meteringdevice'
DEVICE_NAME = 'test-device'
CABLE_NAME = 'test-cable'

mdguid = None

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def setup():
    global mdguid, cableguid
    mdguid = racktivity_test_library.meteringdevice.create(METERINGDEVICE_NAME, 'M1', getRackGuid(),
                                                           poweroutputsnumber=1)
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testConnectDisconnectOutputPort_1():
    """
    @description: [0.16.01.01] Test Connect/Disconnect Power Output port
    @id: 0.16.01.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.disconnectPowerOutputPort(guid, 'label')
             cloudapi.meteringdevice.connectPowerOutputPort(guid, 'label', cableguid)
    @expected_result: The test should succeed in connectiong/disconnection an output power port using a created cable
              
    """
    cloudapi = getCloudapi()
    cableguid = racktivity_test_library.cable.create(CABLE_NAME)
    cloudapi.meteringdevice.connectPowerOutputPort(getMeteringdeviceGuid(), 'output-1', cableguid)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    outputport = None
    for port in md.poweroutputs:
        if port.label == 'output-1':
            outputport = port
            break
        
    assert_true(outputport, "Failed to find power output")
    assert_equal(outputport.cableguid, cableguid, "Failed to connect port, (cable guid wasn't set correctly)")
    
    cloudapi.meteringdevice.disconnectPowerOutputPort(getMeteringdeviceGuid(), 'output-1')
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    outputport = None
    for port in md.poweroutputs:
        if port.label == 'output-1':
            outputport = port
            break
    
    assert_true(outputport, "Failed to find power output")
    assert_equal(outputport.cableguid, None, "Failed to disconnect port, (cable guid wasn't set correctly)")
    
    #the cable should be deleted afterwards.
    assert_raises(CloudApiException, cloudapi.cable.getObject, cableguid)
    
def testDisconnectOutputPort_2():
    """
    @description: [0.16.01.02] Test Disconnect Power Output port with cableguid
    @id: 0.16.01.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.disconnectPowerOutputPort(guid, cableguid=cableguid)
    @expected_result: The test should succeed in connectiong/disconnection an output power port using a created cable
    """
    cloudapi = getCloudapi()
    cableguid = racktivity_test_library.cable.create(CABLE_NAME)
    cloudapi.meteringdevice.connectPowerOutputPort(getMeteringdeviceGuid(), 'output-1', cableguid)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    outputport = None
    for port in md.poweroutputs:
        if port.label == 'output-1':
            outputport = port
            break
        
    assert_true(outputport, "Failed to find power output")
    assert_equal(outputport.cableguid, cableguid, "Failed to connect port, (cable guid wasn't set correctly)")
    
    cloudapi.meteringdevice.disconnectPowerOutputPort(getMeteringdeviceGuid(), cableguid=cableguid)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    outputport = None
    for port in md.poweroutputs:
        if port.label == 'output-1':
            outputport = port
            break
    
    assert_true(outputport, "Failed to find power output")
    assert_equal(outputport.cableguid, None, "Failed to disconnect port, (cable guid wasn't set correctly)")
    
    assert_raises(CloudApiException, cloudapi.cable.getObject, cableguid)

def testConnectOutputPort_3():
    """
    @description: [0.16.01.03] Test Connect using a not existing label
    @id: 0.16.01.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.connectPowerOutputPort(guid, 'wronglabel', cableguid)
    @expected_result: The test should fail in connectiong the output power port
    """
    cloudapi = getCloudapi()
    assert_raises(CloudApiException, cloudapi.meteringdevice.connectPowerOutputPort, getMeteringdeviceGuid(), 'output-1234', EMPTY_GUID)
    
