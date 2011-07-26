from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, backplaneGuid
    data = getData()
    ca = data["ca"]
    backplaneGuid = racktivity_test_library.backplane.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [0020301] Deleting a Previously created backplane
    @id: 0020301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.delete(backplaneGuid)
    @expected_result: the backplane should be deleted
    """
    q.logger.log("    Deleting Previously created backplane")
    ca.backplane.delete(backplaneGuid)
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.backplane.getObject, backplaneGuid)

@raises(cloud_api_client.Exceptions.CloudApiException)
def testDelete_2():
    """
    @description: [0020302] Deleting a non existing backplane
    @id: 0020302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the backplane doesn't exist
    """
    q.logger.log("    Deleting non existing backplane")
    ca.backplane.delete('00000000-0000-0000-0000-000000000000')

