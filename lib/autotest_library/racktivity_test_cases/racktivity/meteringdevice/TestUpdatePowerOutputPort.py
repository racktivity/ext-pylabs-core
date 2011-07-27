from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid, getEmulatorConfig

DEVICE_NAME = 'test-meteringdevice'
IPADDRESS_NAME = 'test-localip'

mdguid = None

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def getMeteringdeviceGuid():
    global pmguid
    return pmguid

def setup():
    global pmguid, mdguid
    ip,port,type = getEmulatorConfig()
    ipaddressguid = racktivity_test_library.ipaddress.create(IPADDRESS_NAME, ip)
    mdguid, pmguid = racktivity_test_library.meteringdevice.createRacktivity(DEVICE_NAME, getRackGuid(),
                                                                   ipaddressguid=ipaddressguid,
                                                                   meteringdevicetype=type,
                                                                   port=port)
    
def teardown():
    global mdguid
    racktivity_test_library.meteringdevice.delete(mdguid)
    
def testUpdatePowerOutputLabel_1():
    """
    @description: [0.16.20.01] Test Update Power Output label
    @id: 0.16.20.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerOutputPort(guid, label, newlabel)
    @expected_result: Power output label is updated
    """
    cloudapi = getCloudapi()
    portlabel = 'output-1'
    newportlabel = 'newlabel'
    cloudapi.meteringdevice.updatePowerOutputPort(getMeteringdeviceGuid(), portlabel, newportlabel)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    
    powerport = None
    for port in md.poweroutputs:
        if port.label == newportlabel:
            powerport = port
            break
    
    assert_true(powerport, "Updating port label failed (no port found with the new label)")
    cloudapi.meteringdevice.updatePowerOutputPort(getMeteringdeviceGuid(), newportlabel, portlabel)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    powerport = None
    for port in md.poweroutputs:
        if port.label == portlabel:
            powerport = port
            break
    
    assert_true(powerport, "Restoring port label failed (no port found with the port label)")
    
def testUpdatePowerOutputLabel_2():
    """
    @description: [0.16.20.02] Test Update Power Output label with a duplicate label
    @id: 0.16.20.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerOutputPort(guid, label, newduplicatelabel)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    portlabel = 'output-1'
    newportlabel = 'output-2'
    assert_raises(Fault, cloudapi.meteringdevice.updatePowerOutputPort, getMeteringdeviceGuid(), portlabel, newportlabel)

def testUpdatePowerOutputSequence_3():
    """
    @description: [0.16.20.03] Test Update Power Output sequence
    @id: 0.16.20.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerOutputPort(guid, label, sequence=newsequence)
    @expected_result: Power output sequence number is updated
    """
    cloudapi = getCloudapi()
    portlabel = 'output-1'
    sequence = 1
    newsequence = 10
    cloudapi.meteringdevice.updatePowerOutputPort(getMeteringdeviceGuid(), portlabel, sequence=newsequence)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    
    powerport = None
    for port in md.poweroutputs:
        if port.sequence == newsequence:
            powerport = port
            break
    
    assert_true(powerport, "Updating port sequence failed (no port found with the new new sequence)")
    cloudapi.meteringdevice.updatePowerOutputPort(getMeteringdeviceGuid(), portlabel, sequence=sequence)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    powerport = None
    for port in md.poweroutputs:
        if port.sequence == sequence:
            powerport = port
            break
    
    assert_true(powerport, "Restoring port sequence failed (no port found with the port new sequence)")
    
def testUpdatePowerOutputSequence_4():
    """
    @description: [0.16.20.04] Test Update Power Output sequence with a duplicate sequence
    @id: 0.16.20.04
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updatePowerOutputPort(guid, label, sequence=newduplicatesequence)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    portlabel = 'output-1'
    assert_raises(Fault, cloudapi.meteringdevice.updatePowerOutputPort, getMeteringdeviceGuid(), portlabel, sequence=2)
