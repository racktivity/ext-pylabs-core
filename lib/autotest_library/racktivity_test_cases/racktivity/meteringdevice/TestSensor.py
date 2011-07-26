from nose.tools import *
from cloud_api_client.Exceptions import CloudApiException
import racktivity_test_library
from pymonkey import i, q
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'
SENSOR_LABEL_ONE = 'sensor-label-1'
SENSOR_LABEL_TWO = 'sensor-label-2'

mdguid = None

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def setup():
    global mdguid
    mdguid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid())
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())
    
def testAddDeleteSensor_1():
    """
    @description: [0.16.15.01] Test Add/Delete sensor
    @id: 0.16.15.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addSensor(guid, label, type, sequence)
             cloudapi.meteringdevice.deleteSensor(guid, label)
    @expected_result: A sensor is added for the metering device, then it is deleted
              
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addSensor(getMeteringdeviceGuid(), SENSOR_LABEL_ONE, 'TEMPERATURESENSOR', sequence)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    if not md.sensors:
        raise RuntimeError("Failed to add sensor")
    found = False
    for sensor in md.sensors:
        if sensor.sequence == sequence and sensor.label == SENSOR_LABEL_ONE:
            found = True
            break
    assert_true(found, "Failed to add sensor (can't be found in the list of sensors)")
    
    cloudapi.meteringdevice.deleteSensor(getMeteringdeviceGuid(), SENSOR_LABEL_ONE)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    found = False
    for sensor in md.sensors:
        if sensor.sequence == sequence and sensor.label == SENSOR_LABEL_ONE:
            found = True
            break
    
    assert_false(found, "Failed to delete sensor (still available in the list of sensors)")

def testAddSensor_2():
    """
    @description: [0.16.15.02] Test Add/Delete sensor with wrong sequence
    @id: 0.16.15.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addSensor(guid, label, type, wrongsequence)
    @expected_result: Function should fail to add a sensor
    """
    cloudapi = getCloudapi()
    sequence = -2
    assert_raises(CloudApiException, cloudapi.meteringdevice.addSensor, getMeteringdeviceGuid(), SENSOR_LABEL_ONE, 'TEMPERATURESENSOR', sequence)

def testAddSensor_3():
    """
    @description: [0.16.15.03] Test Add/Delete sensor with wrong type
    @id: 0.16.15.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addSensor(guid, label, wrongtype, sequence)
    @expected_result: Function should fail to add a sensor
    """
    cloudapi = getCloudapi()
    sequence = -2
    assert_raises(CloudApiException, cloudapi.meteringdevice.addSensor, getMeteringdeviceGuid(), SENSOR_LABEL_ONE, 'WRONGSENSOR', sequence)
    
def testAddSensor_4():
    """
    @description: [0.16.15.04] Test Add/Delete sensor with duplicate sequence
    @id: 0.16.15.04
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addSensor(guid, label, type, duplicatesequence)
    @expected_result: Function should fail to add a sensor
    """
    cloudapi = getCloudapi()
    sequence = 1
    cloudapi.meteringdevice.addSensor(getMeteringdeviceGuid(), SENSOR_LABEL_ONE, 'TEMPERATURESENSOR', sequence)
    assert_raises(CloudApiException, cloudapi.meteringdevice.addSensor, getMeteringdeviceGuid(), SENSOR_LABEL_TWO, 'TEMPERATURESENSOR', sequence)
    cloudapi.meteringdevice.deleteSensor(getMeteringdeviceGuid(), SENSOR_LABEL_ONE)
    
def testAddSensor_5():
    """
    @description: [0.16.15.05] Test Add/Delete sensor with no sequence
    @id: 0.16.15.05
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.addSensor(guid, label, type)
    @expected_result: The sensors should be added without passing a sequence number to the cloud API
    """
    cloudapi = getCloudapi()
    cloudapi.meteringdevice.addSensor(getMeteringdeviceGuid(), SENSOR_LABEL_ONE, 'TEMPERATURESENSOR')
    cloudapi.meteringdevice.addSensor(getMeteringdeviceGuid(), SENSOR_LABEL_TWO, 'TEMPERATURESENSOR')
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    sequence_one = 0
    sequence_two = 0
    for sensor in md.sensors:
        if sensor.label == SENSOR_LABEL_ONE:
            sequence_one = sensor.sequence
        if sensor.label == SENSOR_LABEL_TWO:
            sequence_two = sensor.sequence
    
    assert_true(sequence_one, "Can't find the first sensor added")
    assert_true(sequence_two, "Can't find the second sensor added")
    assert_equal(sequence_two - sequence_one, 1, "The sequence didn't auto increment")
