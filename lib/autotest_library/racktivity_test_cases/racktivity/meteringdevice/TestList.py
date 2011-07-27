from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'

def getCloudapi():
    return p.api.action.racktivity

def testList_1():
    """
    @description: [0.16.11.01] Test List metering devices
    @id: 0.16.11.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.list()
    @expected_result: the created metering device GUID is found by list action
    """
    cloudapi = getCloudapi()
    guid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid())
    devices = cloudapi.meteringdevice.list()['result']['meteringdeviceinfo']
    assert_true(devices, "No devices listed")
    found = False
    for device in devices:
        if device['guid'] == guid:
            found = True
            break
    assert_true(found, "Device didn't found by list")
    racktivity_test_library.meteringdevice.delete(guid)

