from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'

mdguid = None

def getCloudapi():
    return p.api.action.racktivity

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def setup():
    global mdguid
    mdguid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid(), powerinputsnumber=2)
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testUpdatePowerInputLabel_1():
    """
    @description: [0.16.19.01] Test Update Power Input label
    @id: 0.16.19.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerInputPort(guid, label, newlabel)
    @expected_result: Power input label is updated
    """
    cloudapi = getCloudapi()
    portlabel = 'input-1'
    newportlabel = 'newlabel'
    cloudapi.meteringdevice.updatePowerInputPort(getMeteringdeviceGuid(), portlabel, newportlabel)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    
    powerport = None
    for port in md.powerinputs:
        if port.label == newportlabel:
            powerport = port
            break
    
    assert_true(powerport, "Updating port label failed (no port found with the new label)")
    cloudapi.meteringdevice.updatePowerInputPort(getMeteringdeviceGuid(), newportlabel, portlabel)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    powerport = None
    for port in md.powerinputs:
        if port.label == portlabel:
            powerport = port
            break
    
    assert_true(powerport, "Restoring port label failed (no port found with the port label)")
    
def testUpdatePowerInputLabel_2():
    """
    @description: [0.16.19.02] Test Update Power Input label with a duplicate label
    @id: 0.16.19.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerInputPort(guid, label, newduplicatelabel)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    portlabel = 'input-1'
    newportlabel = 'input-2'
    assert_raises(Fault, cloudapi.meteringdevice.updatePowerInputPort, getMeteringdeviceGuid(), portlabel, newportlabel)

def testUpdatePowerInputSequence_3():
    """
    @description: [0.16.19.03] Test Update Power Input sequence
    @id: 0.16.19.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerInputPort(guid, label, sequence=newsequence)
    @expected_result: Power input sequence number is updated
    """
    cloudapi = getCloudapi()
    portlabel = 'input-1'
    sequence = 1
    newsequence = 10
    cloudapi.meteringdevice.updatePowerInputPort(getMeteringdeviceGuid(), portlabel, sequence=newsequence)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    
    powerport = None
    for port in md.powerinputs:
        if port.sequence == newsequence:
            powerport = port
            break
    
    assert_true(powerport, "Updating port sequence failed (no port found with the new new sequence)")
    cloudapi.meteringdevice.updatePowerInputPort(getMeteringdeviceGuid(), portlabel, sequence=sequence)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    powerport = None
    for port in md.powerinputs:
        if port.sequence == sequence:
            powerport = port
            break
    
    assert_true(powerport, "Restoring port sequence failed (no port found with the port new sequence)")
    
def testUpdatePowerInputSequence_4():
    """
    @description: [0.16.19.04] Test Update Power Input sequence with a duplicate sequence
    @id: 0.16.19.04
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerInputPort(guid, label, sequence=newduplicatesequence)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    portlabel = 'input-1'
    assert_raises(Fault, cloudapi.meteringdevice.updatePowerInputPort, getMeteringdeviceGuid(), portlabel, sequence=2)
