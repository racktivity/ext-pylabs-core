from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q

def setup():
    global cloudapi, guid
    cloudapi = i.config.cloudApiConnection.find("main")
    guid = racktivity_test_library.enterprise.create('test_enterprise1')

def teardown():
    racktivity_test_library.enterprise.delete(guid)
    
def testRemovecampus_1():
    """
    @description: [0.33.21.01] passing a non existing enterprise GUID to the function 
    @id: 0.33.21.01
    @timestamp: 1298553343
    @signature: halimm
    @params: cloudapi.enterprise.removeCampus('00000000-0000-0000-0000-000000000000', guid)
    @expected_result: function should fail because there is no enterprise with that GUID
    """
    q.logger.log("         Removing campus from non existing enterprise")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, cloudapi.enterprise.removeCampus, '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000')

