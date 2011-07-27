from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

RACK_NAME = 'rack-test-device'
DEVICE_NAME = 'test-device'

def getCloudapi():
    return i.config.cloudApiConnection.find('main')
    
def testCreate_1():
    """
    @description: [0.09.02.01] Test Create a device
    @id: 0.09.02.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.create(name, type, rackguid=rackguid)
    @expected_result: Device is created, then deleted
    """
    cloudapi = getCloudapi()
    rackguid = getRackGuid()
    deviceguid = cloudapi.device.create(DEVICE_NAME, devicetype='COMPUTER', rackguid=rackguid)['result']['deviceguid']
    ok_(deviceguid, "Empty guid returned from create function")
    device = cloudapi.device.getObject(deviceguid)
    racktivity_test_library.device.delete(deviceguid)

def testCreate_2():
    """
    @description: [0.09.02.02] Test Create a device with wrong name
    @id: 0.09.02.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.create(1, type, rackguid=rackguid)
    @expected_result: Function should fail with no device created
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.device.create, 1, 'COMPUTER')

def testCreate_3():
    """
    @description: [0.09.02.03] Test Create a device with wrong device type
    @id: 0.09.02.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.device.create(name, wrongtype, rackguid=rackguid)
    @expected_result: Function should fail with no device created
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.device.create, DEVICE_NAME, 'ROBOT')
