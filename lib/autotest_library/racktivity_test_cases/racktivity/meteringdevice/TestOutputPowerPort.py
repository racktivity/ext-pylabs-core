from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'
PORT_LABEL_ONE = 'output-label-1'
PORT_LABEL_TWO = 'output-label-2'

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
    
def testAddDeleteOutputPowerPort_1():
    """
    @description: [0.16.12.01] Test Add/Delete output power port
    @id: 0.16.12.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addOutputPowerPort(guid, label, sequence)
             cloudapi.meteringdevice.deleteOutputPowerPort(guid, label)
    @expected_result: the output power port is created and deleted successfully
              
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, sequence)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    if not md.poweroutputs:
        raise RuntimeError("Failed to add power output")
    found = False
    for output in md.poweroutputs:
        if output.sequence == sequence and output.label == PORT_LABEL_ONE:
            found = True
            break
    assert_true(found, "Failed to add power output (can't be found in the list of output ports)")
    
    cloudapi.meteringdevice.deleteOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    found = False
    for output in md.poweroutputs:
        if output.sequence == sequence and output.label == PORT_LABEL_ONE:
            found = True
            break
    
    assert_false(found, "Failed to delete power output (still available in the list of output ports)")

def testAddOutputPowerPort_2():
    """
    @description: [0.16.12.02] Test Add output power port with wrong sequence
    @id: 0.16.12.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addOutputPowerPort(guid, label, wrongsequence)
    @expected_result: Function should fail because of the invalid sequence number used for the output power port
    """
    cloudapi = getCloudapi()
    sequence = -2
    assert_raises(Fault, cloudapi.meteringdevice.addOutputPowerPort, getMeteringdeviceGuid(), PORT_LABEL_ONE, sequence)

def testAddOutputPowerPort_3():
    """
    @description: [0.16.12.03] Test Add output power port with duplicate sequence
    @id: 0.16.12.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addOutputPowerPort(guid, label, duplicatesequence)
    @expected_result: Function should fail because of the duplicate sequence number used for the output power port
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, sequence)
    assert_raises(Fault, cloudapi.meteringdevice.addOutputPowerPort, getMeteringdeviceGuid(), PORT_LABEL_TWO, sequence)
    cloudapi.meteringdevice.deleteOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    
def testAddOutputPowerPort_4():
    """
    @description: [0.16.12.04] Test Add output power port with no sequence
    @id: 0.16.12.04
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addOutputPowerPort(guid, label)
    @expected_result: the output ports are added to the metering device without no sequence number for the port given to the cloud API
    """
    cloudapi = getCloudapi()
    cloudapi.meteringdevice.addOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    cloudapi.meteringdevice.addOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_TWO)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    sequence_one = 0
    sequence_two = 0
    for output in md.poweroutputs:
        if output.label == PORT_LABEL_ONE:
            sequence_one = output.sequence
        if output.label == PORT_LABEL_TWO:
            sequence_two = output.sequence
    cloudapi.meteringdevice.deleteOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    cloudapi.meteringdevice.deleteOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_TWO)
    assert_true(sequence_one, "Can't find the first port added")
    assert_true(sequence_two, "Can't find the second port added")
    assert_equal(sequence_two - sequence_one, 1, "The sequence didn't auto increment")

def testConnectDisconnectPowerOutputPort_5():
    """
    @description: [0.16.12.05] Test Connect/Disconnect output power port
    @id: 0.16.12.05
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.connectPowerOutputPort(meteringdeviceguid, portlabel, cableguid)
    @expected_result: the output port is connected with the given cable to another device
    """
    cloudapi = getCloudapi()
    cable_name = 'TEST_CABLE'
    cloudapi.meteringdevice.addOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    cableguid = cloudapi.cable.create(cable_name, str(q.enumerators.cabletype.POWERCABLE))['result']['cableguid']
    result = cloudapi.meteringdevice.connectPowerOutputPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, cableguid)['result']['returncode']
    assert_true(result, "Can't connect power output port")
    result = cloudapi.meteringdevice.disconnectPowerOutputPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, cableguid)['result']['returncode']
    cloudapi.meteringdevice.deleteOutputPowerPort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    assert_true(result, "Can't disconnect power output port")
