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
    racktivity_test_library.rack.delete(rackGuid)

def testDiscover_1():
    """
    @description: [0191301] Discovering an energyswitch
    @id: 0191301
    @timestamp: 1293370198
    @signature: mmagdy
    @params: ca.rack.discover(rackGuid, ["192.168.14.133"])
    @expected_result: the rack should be deleted
    """
    IP = "192.168.14.133"
    q.logger.log("    Deleting Previously created rack")
    result = ca.rack.discover(rackGuid, [IP])["result"]["discovered"]
    ok_(result, "Failed to discover device at %s"%IP)
    assert_equals(result[IP]["type"], "racktivity")
