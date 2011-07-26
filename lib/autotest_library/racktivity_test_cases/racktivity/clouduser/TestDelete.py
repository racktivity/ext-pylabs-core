from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, usrGuid
    ca = i.config.cloudApiConnection.find("main")
    usrGuid = racktivity_test_library.clouduser.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [0050301] Deleting Previously created clouduser
    @id: 0050301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.clouduser.delete(usrGuid)
    @expected_result: the clouduser should be deleted
    """
    q.logger.log("    Deleting Previously created clouduser")
    ca.clouduser.delete(usrGuid)
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.clouduser.getObject, usrGuid)

@raises(cloud_api_client.Exceptions.CloudApiException)
def testDelete_2():
    """
    @description: [0050302] Deleting non existing clouduser
    @id: 0050302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the clouduser doesn't exist
    """
    q.logger.log("    Deleting non existing clouduser")
    ca.clouduser.delete('00000000-0000-0000-0000-000000000000')

