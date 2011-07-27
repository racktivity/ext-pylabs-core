from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import q, i
from . import getRackGuid

DEVICE_NAME = 'test-meteringdevice'
EMPTY_GUID = '00000000-0000-0000-0000-000000000000'

def getCloudapi():
    return p.api.action.racktivity

def testDelete_1():
    """
    @description: [0.16.03.01] Test Delete a metering device
    @id: 0.16.03.01
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.delete(guid)
    @expected_result: The metering device is deleted
    """
    guid = racktivity_test_library.meteringdevice.create(DEVICE_NAME, 'M1', getRackGuid())
    cloudapi = getCloudapi()
    md = cloudapi.meteringdevice.getObject(guid)
    assert_true(md, "Create meteringdeivce failed")
    cloudapi.meteringdevice.delete(guid)
    assert_raises(Fault, cloudapi.meteringdevice.getObject, guid)
    racktivity_test_library.ui.doUITest(md.rackguid, "DELETE", value=md.name)
    ok_(racktivity_test_library.ui.getResult(md.name))

def testDelete_2():
    """
    @description: [0.16.03.02] Test Delete a metering device with wrong guid
    @id: 0.16.03.02
    @timestamp: 1293360198
    @signature: helmyr
    @params: cloudapi.meteringdevice.delete(wrongguid)
    @expected_result: Nothing happens to the metering device model
    """
    cloudapi = getCloudapi()
    assert_raises(Fault, cloudapi.meteringdevice.delete, EMPTY_GUID)
