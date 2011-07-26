from nose.tools import *
from cloud_api_client.Exceptions import CloudApiException
import racktivity_test_library
from pymonkey import i, q
from . import getRackGuid

RACK_NAME = 'rack-test-device'
DEVICE_NAME = 'test-device'

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def testList_1():
    """
    @description: [0.09.11.01] Test device List
    @id: 0.09.11.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.list(deviceguid=guid)
    @expected_result: device info is returned given its GUID
    """
    cloudapi = getCloudapi()
    guid = racktivity_test_library.device.create(DEVICE_NAME, getRackGuid())
    devices = cloudapi.device.list(deviceguid=guid)['result']['deviceinfo']
    assert_true(devices, "No devices listed")
    found = False
    for device in devices:
        if device['guid'] == guid:
            found = True
            break
    assert_true(found, "Device didn't found by list")
    racktivity_test_library.device.delete(guid)

