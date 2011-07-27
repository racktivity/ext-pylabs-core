from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'
PORT_LABEL_ONE = 'port-label-1'
PORT_LABEL_TWO = 'port-label-2'

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
    
def testAddDeletePort_1():
    """
    @description: [0.16.13.01] Test Add/Delete port
    @id: 0.16.13.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addPort(guid, label, type, sequence)
             cloudapi.meteringdevice.deletePort(guid, label)
    @expected_result: A port is added to the metering device, and then deleted
              
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, 'SERIAL', sequence)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    if not md.ports:
        raise RuntimeError("Failed to add port")
    found = False
    for port in md.ports:
        if port.sequence == sequence and port.label == PORT_LABEL_ONE:
            found = True
            break
    assert_true(found, "Failed to add port (can't be found in the list of ports)")
    
    cloudapi.meteringdevice.deletePort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    found = False
    for port in md.ports:
        if port.sequence == sequence and port.label == PORT_LABEL_ONE:
            found = True
            break
    
    assert_false(found, "Failed to delete port (still available in the list of ports)")

def testAddPort_2():
    """
    @description: [0.16.13.02] Test Add/Delete port with wrong sequence
    @id: 0.16.13.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addPort(guid, label, type, wrongsequence)
    @expected_result: Function should fail in adding the port
    """
    cloudapi = getCloudapi()
    sequence = -2
    assert_raises(Fault, cloudapi.meteringdevice.addPort, getMeteringdeviceGuid(), PORT_LABEL_ONE, 'SERIAL', sequence)

def testAddPort_3():
    """
    @description: [0.16.13.03] Test Add/Delete port with wrong type
    @id: 0.16.13.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addPort(guid, label, wrongtype, sequence)
    @expected_result: Function should fail in adding the port
    """
    cloudapi = getCloudapi()
    sequence = -2
    assert_raises(Fault, cloudapi.meteringdevice.addPort, getMeteringdeviceGuid(), PORT_LABEL_ONE, 'PARALLEL', sequence)
    
def testAddPort_4():
    """
    @description: [0.16.13.04] Test Add/Delete port with duplicate sequence
    @id: 0.16.13.04
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addPort(guid, label, type, duplicatesequence)
    @expected_result: Function should fail in adding the port
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, 'SERIAL', sequence)
    assert_raises(Fault, cloudapi.meteringdevice.addPort, getMeteringdeviceGuid(), PORT_LABEL_TWO, 'SERIAL', sequence)
    cloudapi.meteringdevice.deletePort(getMeteringdeviceGuid(), PORT_LABEL_ONE)
    
def testAddPort_5():
    """
    @description: [0.16.13.05] Test Add/Delete port with no sequence
    @id: 0.16.13.05
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addPort(guid, label, type)
    @expected_result: The ports should be added to the metering device without passing a sequence number to the cloud API
    """
    cloudapi = getCloudapi()
    cloudapi.meteringdevice.addPort(getMeteringdeviceGuid(), PORT_LABEL_ONE, 'SERIAL')
    cloudapi.meteringdevice.addPort(getMeteringdeviceGuid(), PORT_LABEL_TWO, 'SERIAL')
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    sequence_one = 0
    sequence_two = 0
    for port in md.ports:
        if port.label == PORT_LABEL_ONE:
            sequence_one = port.sequence
        if port.label == PORT_LABEL_TWO:
            sequence_two = port.sequence
    
    assert_true(sequence_one, "Can't find the first port added")
    assert_true(sequence_two, "Can't find the second port added")
    assert_equal(sequence_two - sequence_one, 1, "The sequence didn't auto increment")
