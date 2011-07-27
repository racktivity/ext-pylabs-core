from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'
PORT_LABEL_ONE = 'input-label-1'
PORT_LABEL_TWO = 'input-label-2'

mdguid = None

def getCloudapi():
    return p.api.action.racktivity

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def setup():
    global mdguid
    mdguid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid())
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testAddDeleteInputPowerPort_1():
    """
    @description: [0.16.09.01] Test Add/Delete input power port
    @id: 0.16.09.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addInputPowerPort(guid, label, sequence)
             cloudapi.meteringdevice.deleteInputPowerPort(guid, label)
    @expected_result: An input power port should be added/deleted to the metering device
              
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, sequence)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    if not md.powerinputs:
        raise RuntimeError("Failed to add power input")
    found = False
    for input in md.powerinputs:
        if input.sequence == sequence and input.label == PORT_LABEL_ONE:
            found = True
            break
    assert_true(found, "Failed to add power input (can't be found in the list of input ports)")
    
    cloudapi.meteringdevice.deleteInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    found = False
    for input in md.powerinputs:
        if input.sequence == sequence and input.label == PORT_LABEL_ONE:
            found = True
            break
    
    assert_false(found, "Failed to delete power input (still available in the list of input ports)")

def testAddInputPowerPort_2():
    """
    @description: [0.16.09.02] Test Add input power port with wrong sequence
    @id: 0.16.09.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addInputPowerPort(guid, label, wrongsequence)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    sequence = -2
    assert_raises(Fault, cloudapi.meteringdevice.addInputPowerPort, getMeteringdeviceGuid(), PORT_LABEL_ONE, sequence)

def testAddInputPowerPort_3():
    """
    @description: [0.16.09.03] Test Add input power port with duplicate sequence
    @id: 0.16.09.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addInputPowerPort(guid, label, duplicatesequence)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, sequence)
    assert_raises(Fault, cloudapi.meteringdevice.addInputPowerPort, getMeteringdeviceGuid(), PORT_LABEL_TWO, sequence)
    cloudapi.meteringdevice.deleteInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    
def testAddInputPowerPort_4():
    """
    @description: [0.16.09.04] Test Add input power port with no sequence
    @id: 0.16.09.04
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addInputPowerPort(guid, label)
    @expected_result: 2 input power ports are added without specifying a sequence number
    """
    cloudapi = getCloudapi()
    cloudapi.meteringdevice.addInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    cloudapi.meteringdevice.addInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_TWO)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    sequence_one = 0
    sequence_two = 0
    for input in md.powerinputs:
        if input.label == PORT_LABEL_ONE:
            sequence_one = input.sequence
        if input.label == PORT_LABEL_TWO:
            sequence_two = input.sequence
    cloudapi.meteringdevice.deleteInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    cloudapi.meteringdevice.deleteInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_TWO)
    assert_true(sequence_one, "Can't find the first port added")
    assert_true(sequence_two, "Can't find the second port added")
    assert_equal(sequence_two - sequence_one, 1, "The sequence didn't auto increment")
    
def testConnectDisconnectPowerInputPort_5():
    """
    @description: [0.16.09.05] Test Connect/Disconnect input power port
    @id: 0.16.09.05
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.connectPowerInputPort(meteringdeviceguid, portlabel, cableguid)
    @expected_result: the input port is connected with the given cable to another device
    """
    cloudapi = getCloudapi()
    cable_name = 'TEST_CABLE'
    cloudapi.meteringdevice.addInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    cableguid = cloudapi.cable.create(cable_name, str(q.enumerators.cabletype.POWERCABLE))['result']['cableguid']
    result = cloudapi.meteringdevice.connectPowerInputPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, cableguid)['result']['returncode']
    assert_true(result, "Can't connect power input port")
    result = cloudapi.meteringdevice.disconnectPowerInputPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, cableguid)['result']['returncode']
    assert_true(result, "Can't disconnect power input port")
    cloudapi.meteringdevice.deleteInputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
