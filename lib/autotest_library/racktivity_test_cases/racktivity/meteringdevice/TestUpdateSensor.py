from nose.tools import *
from cloud_api_client.Exceptions import CloudApiException
import racktivity_test_library
from pymonkey import i, q
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'

mdguid = None

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def setup():
    global mdguid
    mdguid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid(), sensorsnumber=2)
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testUpdateSensorLabel_1():
    """
    @description: [0.16.22.01] Test Update sensor label
    @id: 0.16.22.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updateSensor(guid, sensorlabel, newsensorlabel)
    @expected_result: Sensor label is updated
    """
    cloudapi = getCloudapi()
    sensorlabel = 'sensor-1'
    newsensorlabel = 'newlabel'
    cloudapi.meteringdevice.updateSensor(getMeteringdeviceGuid(), sensorlabel, newsensorlabel)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    
    sensor = None
    for s in md.sensors:
        if s.label == newsensorlabel:
            sensor = s
            break
    
    assert_true(sensor, "Updating sensor label failed (no sensor found with the new label)")
    cloudapi.meteringdevice.updateSensor(getMeteringdeviceGuid(), newsensorlabel, sensorlabel)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    sensor = None
    for s in md.sensors:
        if s.label == sensorlabel:
            sensor = s
            break
    
    assert_true(sensor, "Restoring sensor label failed (no sensor found with the s label)")
    
def testUpdateSensorLabel_2():
    """
    @description: [0.16.22.02] Test Update sensor label with duplicate label
    @id: 0.16.22.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updateSensor(guid, sensorlabel, newsensorlabel)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    sensorlabel = 'sensor-1'
    newsensorlabel = 'sensor-2'
    assert_raises(CloudApiException, cloudapi.meteringdevice.updateSensor, getMeteringdeviceGuid(), sensorlabel, newsensorlabel)

def testUpdateSensorSequence_3():
    """
    @description: [0.16.22.03] Test Update sensor sequence
    @id: 0.16.22.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updateSensor(guid, sensorlabel, sequence=newsequence)
    @expected_result: Sensor sequence number is updated
    """
    cloudapi = getCloudapi()
    sensorlabel = 'sensor-1'
    sequence = 1
    newsequence = 10
    cloudapi.meteringdevice.updateSensor(getMeteringdeviceGuid(), sensorlabel, sequence=newsequence)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    
    sensor = None
    for s in md.sensors:
        if s.sequence == newsequence:
            sensor = s
            break
    
    assert_true(sensor, "Updating sensor sequence failed (no s found with the new new sequence)")
    cloudapi.meteringdevice.updateSensor(getMeteringdeviceGuid(), sensorlabel, sequence=sequence)
    
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    sensor = None
    for s in md.sensors:
        if s.sequence == sequence:
            sensor = s
            break
    
    assert_true(sensor, "Restoring sensor sequence failed (no s found with the s new sequence)")
    
def testUpdateSensorSequence_4():
    """
    @description: [0.16.22.04] Test Update sensor sequence with duplicate seuqnce
    @id: 0.16.22.04
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updateSensor(guid, sensorlabel, sequence=newduplicatesequence)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    sensorlabel = 'sensor-1'
    assert_raises(CloudApiException, cloudapi.meteringdevice.updateSensor, getMeteringdeviceGuid(), sensorlabel, sequence=2)
