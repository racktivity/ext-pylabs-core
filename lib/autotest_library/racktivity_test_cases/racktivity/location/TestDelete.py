from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, locGuid
    ca = i.config.cloudApiConnection.find("main")
    locGuid = racktivity_test_library.location.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [0150301] Deleting Previously created location
    @id: 0150301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.delete(locGuid)
    @expected_result: delete operation succeed and this location's info/object can no longer be retrieved from the drp
    """
    q.logger.log("    Deleting Previously created location")
    ca.location.delete(locGuid)
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.location.getObject, locGuid)


@raises(cloud_api_client.Exceptions.CloudApiException)
def testDelete_2():
    """
    @description: [0150302] Deleting non existing location
    @id: 0150302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: delete operation fails because the guid is invalid
    """
    q.logger.log("    Deleting non existing location")
    ca.location.delete('00000000-0000-0000-0000-000000000000')

