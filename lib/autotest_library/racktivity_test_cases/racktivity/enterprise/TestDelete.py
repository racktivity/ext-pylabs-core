from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global cloudapi, guid
    cloudapi = i.config.cloudApiConnection.find("main")
    
def teardown():
    pass

def testDelete_1():
    """
    @description: [0.33.03.01] Deleting Previously created enterprise
    @id: 0.33.03.01
    @timestamp: 1298553343
    @signature: halimm
    @params: cloudapi.enterprise.delete(guid)
    @expected_result:the enterprise should be deleted
    """
    guid = racktivity_test_library.enterprise.create('test_enterprise1')
    q.logger.log("    Deleting Previously created enterprise")
    cloudapi.enterprise.delete(guid)
    assert_raises(xmlrpclib.Fault, cloudapi.enterprise.getObject, guid)

def testDelete_2():
    """
    @description: [0.33.03.02] Deleting non existing enterprise
    @id: 0.33.03.02
    @timestamp: 1298553343
    @signature: halimm
    @params: cloudapi.enterprise.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the enterprise doesn't exist
    """
    q.logger.log("    Deleting non existing enterprise")
    assert_raises(xmlrpclib.Fault, cloudapi.enterprise.delete, '00000000-0000-0000-0000-000000000000')


