from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, rackGuid,roomguid
    data = getData()
    ca = data["ca"]
    roomguid = data["roomguid"]
    rackGuid = racktivity_test_library.rack.create("test_rack1", roomguid)

def teardown():
    pass

def testDelete_1():
    """
    @description: [0190301] Deleting Previously created rack
    @id: 0190301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.delete(rackGuid)
    @expected_result: the rack should be deleted
    """
    q.logger.log("    Deleting Previously created rack")
    rack1 = ca.rack.getObject(rackGuid)
    ca.rack.delete(rackGuid)
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.rack.getObject, rackGuid)
    racktivity_test_library.ui.doUITest(rack1.roomguid, "DELETE", value=rack1.name)
    ok_(racktivity_test_library.ui.getResult(rack1.name))

@raises(cloud_api_client.Exceptions.CloudApiException)
def testDelete_2():
    """
    @description: [0190302] Deleting non existing rack
    @id: 0190302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: the rack should be deleted
    """
    q.logger.log("    Deleting non existing rack")
    ca.rack.delete('00000000-0000-0000-0000-000000000000')

