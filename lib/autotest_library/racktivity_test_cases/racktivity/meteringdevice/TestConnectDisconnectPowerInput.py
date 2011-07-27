from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

EMPTY_GUID = '00000000-0000-0000-0000-000000000000'
METERINGDEVICE_NAME = 'test-meteringdevice'
DEVICE_NAME = 'test-device'
CABLE_NAME = 'test-cable'

mdguid = None

def getCloudapi():
    return p.api.action.racktivity

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def setup():
    global mdguid, cableguid
    mdguid = racktivity_test_library.meteringdevice.create(METERINGDEVICE_NAME, 'M1', getRackGuid(),
                                                           powerinputsnumber=1)
    
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testConnectDisconnectInputPort_1():
    """
    @description: [0.16.00.01] Test Connect/Disconnect Power Input port
    @id: 0.16.00.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.disconnectPowerInputPort(guid, 'label')
             cloudapi.meteringdevice.connectPowerInputPort(guid, 'label', cableguid)
    @expected_result: The test should succeed in connecting and disconnecting an input port using a newly created cable
    """
    cloudapi = getCloudapi()
    cableguid = racktivity_test_library.cable.create(CABLE_NAME)
    cloudapi.meteringdevice.connectPowerInputPort(getMeteringdeviceGuid(), 'input-1', cableguid)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    inputport = None
    for port in md.powerinputs:
        if port.label == 'input-1':
            inputport = port
            break
        
    assert_true(inputport, "Failed to find power input")
    assert_equal(inputport.cableguid, cableguid, "Failed to connect port, (cable guid wasn't set correctly)")
    
    cloudapi.meteringdevice.disconnectPowerInputPort(getMeteringdeviceGuid(), 'input-1')
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    inputport = None
    for port in md.powerinputs:
        if port.label == 'input-1':
            inputport = port
            break
    
    assert_true(inputport, "Failed to find power input")
    assert_equal(inputport.cableguid, None, "Failed to disconnect port, (cable guid wasn't set correctly)")
    
    #the cable should be deleted afterwards.
    assert_raises(Fault, cloudapi.cable.getObject, cableguid)
    
def testDisconnectInputPort_2():
    """
    @description: [0.16.00.02] Test Disconnect Power Input port with cableguid
    @id: 0.16.00.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.disconnectPowerInputPort(guid, cableguid=cableguid)
    @expected_result: The test should succeed in connecting/disconnecting an input power port using a newly created cable
    """
    cloudapi = getCloudapi()
    cableguid = racktivity_test_library.cable.create(CABLE_NAME)
    cloudapi.meteringdevice.connectPowerInputPort(getMeteringdeviceGuid(), 'input-1', cableguid)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    inputport = None
    for port in md.powerinputs:
        if port.label == 'input-1':
            inputport = port
            break
        
    assert_true(inputport, "Failed to find power input")
    assert_equal(inputport.cableguid, cableguid, "Failed to connect port, (cable guid wasn't set correctly)")
    
    cloudapi.meteringdevice.disconnectPowerInputPort(getMeteringdeviceGuid(), cableguid=cableguid)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    inputport = None
    for port in md.powerinputs:
        if port.label == 'input-1':
            inputport = port
            break
    
    assert_true(inputport, "Failed to find power input")
    assert_equal(inputport.cableguid, None, "Failed to disconnect port, (cable guid wasn't set correctly)")
    
    assert_raises(Fault, cloudapi.cable.getObject, cableguid)

def testConnectInputPort_3():
    """
    @description: [0.16.00.03] Test Connect using an unexisting label
    @id: 0.16.00.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.connectPowerInputPort(guid, 'wronglabel', cableguid)
    @expected_result: the test should fail because the cable does not exist
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.meteringdevice.connectPowerInputPort, getMeteringdeviceGuid(), 'input-1234', EMPTY_GUID)
    
