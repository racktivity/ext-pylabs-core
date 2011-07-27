from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

RACK_NAME = 'rack-test-device'
DEVICE_NAME = 'test-device'

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def testFind_1():
    """
    @description: [0.09.04.01] Test device Find
    @id: 0.09.04.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.find(name=name)
    @expected_result: A device is found given its name
    """
    cloudapi = getCloudapi()
    guid = racktivity_test_library.device.create(DEVICE_NAME, getRackGuid())
    guids = cloudapi.device.find(name=DEVICE_NAME)['result']['guidlist']
    assert_true(guids, "No guids found")
    assert_true(guid in guids, "Find didn't return the correct guid of the device")
    racktivity_test_library.device.delete(guid)

