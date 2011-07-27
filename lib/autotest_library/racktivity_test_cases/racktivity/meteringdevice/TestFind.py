from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'

def getCloudapi():
    return p.api.action.racktivity

def testFind_1():
    """
    @description: [0.16.04.01] Test finding a meteringdevice with its name
    @id: 0.16.04.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.find(name=name)
    @expected_result: the metering device is found given its name
    """
    cloudapi = getCloudapi()
    guid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid())
    guids = cloudapi.meteringdevice.find(name=DEVICE_NAME)['result']['guidlist']
    assert_true(guids, "No guids found")
    assert_true(guid in guids, "Find didn't return the correct guid of the meteringdevice")
    racktivity_test_library.meteringdevice.delete(guid)

