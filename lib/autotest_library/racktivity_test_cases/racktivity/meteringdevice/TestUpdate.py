from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'

meteringdeviceguid = None

def getCloudapi():
    return p.api.action.racktivity

def getMeteringDeviceGuid(name=DEVICE_NAME):
    global meteringdeviceguid
    return meteringdeviceguid

def setup():
    global meteringdeviceguid
    meteringdeviceguid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid())

def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringDeviceGuid())

def testUpdate_1():
    """
    @description: [0.16.21.01] Test Update metering device
    @id: 0.16.21.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updateModelProperties(guid, name=newname)
    @expected_result: The metering device model is updated
    """
    cloudapi = getCloudapi()
    guid = getMeteringDeviceGuid()
    newname = "test-device-renamed"
    cloudapi.meteringdevice.updateModelProperties(guid, name=newname)
    device = cloudapi.meteringdevice.getObject(guid)
    assert_equal(device.name, newname, "Name didn't change")
    #restore device name
    cloudapi.meteringdevice.updateModelProperties(guid, name=DEVICE_NAME)

def testUpdate_2():
    """
    @description: [0.16.21.02] Test Update metering device with wrong name
    @id: 0.16.21.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.updateModelProperties(guid, name=10)
    @expected_result: Function should fail
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.meteringdevice.updateModelProperties, getMeteringDeviceGuid(), name=10)
