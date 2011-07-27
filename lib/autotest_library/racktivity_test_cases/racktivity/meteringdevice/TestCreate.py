from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'

def getCloudapi():
    return i.config.cloudApiConnection.find('main')

def testCreate_1():
    """
    @description: [0.16.02.01] Test Create a metering device
    @id: 0.16.02.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.create(name, id, type, rackguid=rackguid)
    @expected_result: The test should create a metering device successfully
    """
    cloudapi = getCloudapi()
    rackguid = getRackGuid()
    deviceguid = cloudapi.meteringdevice.create(DEVICE_NAME, id='M1', meteringdevicetype='PM0816', template=False, rackguid=rackguid)['result']['meteringdeviceguid']
    ok_(deviceguid, "Empty guid returned from create function")
    device = cloudapi.meteringdevice.getObject(deviceguid)
    racktivity_test_library.ui.doUITest(device.rackguid, "CREATE", value=device.name)
    ok_(racktivity_test_library.ui.getResult(device.name))
    racktivity_test_library.meteringdevice.delete(deviceguid)

def testCreate_2():
    """
    @description: [0.16.02.02] Test Create a metering device with wrong name
    @id: 0.16.02.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.create(1, id, type, rackguid=rackguid)
    @expected_result: The test should fail in creating a metering device
    """
    cloudapi = getCloudapi()
    rackguid = getRackGuid()
    assert_raises(Fault, cloudapi.meteringdevice.create, name=1, id='M1', meteringdevicetype='PM0816', template=False, rackguid=rackguid)

def testCreate_3():
    """
    @description: [0.16.02.03] Test Create a metering device with wrong name
    @id: 0.16.02.03
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.create(name, id, wrongtype, rackguid=rackguid)
    @expected_result: The test should fail in creating a metering device
    """
    cloudapi = getCloudapi()
    rackguid = getRackGuid()
    assert_raises(Fault, cloudapi.meteringdevice.create, name=1, id='M1', meteringdevicetype='DELL_E5500', template=False, rackguid=rackguid)
