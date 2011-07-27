from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import q, i
from . import getRackGuid

RACK_NAME = 'rack-test-device'
DEVICE_NAME = 'test-device'
EMPTY_GUID = '00000000-0000-0000-0000-000000000000'

def getCloudapi():
    return p.api.action.racktivity

def testDelete_1():
    """
    @description: [0.09.03.01] Test device delete
    @id: 0.09.03.01
    @timestamp: 1293360198
    @signature: helmyr
    @params:  cloudapi.device.delete(guid)
    @expected_result: A device is created and deleted successfully 
    """
    guid = racktivity_test_library.device.create(DEVICE_NAME, getRackGuid())
    cloudapi = getCloudapi()
    cloudapi.device.delete(guid)
    devices = cloudapi.device.list(deviceguid=guid)['result']['deviceinfo']
    assert_false(devices, "Delete device faild")

def testDelete_2():
    """
    @description: [0.09.03.02] Test device delete with bad guid
    @id: 0.09.03.02
    @timestamp: 1293360198
    @signature: helmyr
    @params:  cloudapi.device.delete(badguid)
    @expected_result: Function should fail trying to delete a non existing device
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.device.delete, EMPTY_GUID)
