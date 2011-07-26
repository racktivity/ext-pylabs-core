from nose.tools import *
from cloud_api_client.Exceptions import CloudApiException
import racktivity_test_library
from pymonkey import i, q
from . import getRackGuid

RACK_NAME = 'rack-test-device'
DEVICE_NAME = 'test-device'

deviceguid = None

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def getDeviceGuid():
    global deviceguid
    return deviceguid

def setup():
    global deviceguid
    deviceguid = racktivity_test_library.device.create(DEVICE_NAME, getRackGuid())

def teardown():
    racktivity_test_library.device.delete(getDeviceGuid())

def testUpdate_1():
    """
    @description: [0.09.21.01] Test device Update
    @id: 0.09.21.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.updateModelProperties(guid, name=newname, description=description)
    @expected_result: Devie model is updated 
    """
    cloudapi = getCloudapi()
    guid = getDeviceGuid()
    newname = "test-device-renamed"
    description = "test-new-description"
    cloudapi.device.updateModelProperties(guid, name=newname, description=description)
    device = cloudapi.device.getObject(guid)
    assert_equal(device.name, newname, "Name didn't change")
    assert_equal(device.description, description, "Description didn't change")
    #restore device name
    cloudapi.device.updateModelProperties(guid, name=DEVICE_NAME)

def testUpdate_2():
    """
    @description: [0.09.21.02] Test device Update with wrong name
    @id: 0.09.21.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.updateModelProperties(guid, name=1, description=description)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    assert_raises(CloudApiException, cloudapi.device.updateModelProperties, getDeviceGuid(), name=10)

def testUpdate_3():
    """
    @description: [0.09.21.03] Test device Update with wrong device type
    @id: 0.09.21.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.updateModelProperties(guid, devicetype=wrongtype, description=description)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    assert_raises(CloudApiException, cloudapi.device.updateModelProperties, getDeviceGuid(), devicetype='ROBOT')
    
