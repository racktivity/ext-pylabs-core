from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p

def setup():
    global cloudapi, guid
    cloudapi = i.config.cloudApiConnection.find("main")
    guid = racktivity_test_library.enterprise.create('test_enterprise1')

def teardown():
    racktivity_test_library.enterprise.delete(guid)
    
def testAddcampus_1():
    """
    @description: [0.33.20.01] passing a non existing enterprise GUID to the function 
    @id: 0.33.20.01
    @timestamp: 1298553343
    @signature: halimm
    @params: cloudapi.enterprise.addCampus('00000000-0000-0000-0000-000000000000', locGuid1)
    @expected_result: function should fail because there is no enterprise with that GUID
    """
    q.logger.log("         Adding campus to non existing enterprise")
    assert_raises(xmlrpclib.Fault, cloudapi.enterprise.addCampus, '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000')

def testAddcampus_2():
    """
    @description: [0.33.20.02] passing a non existing campus GUID to the function
    @id: 0.33.20.02
    @timestamp: 1298553343
    @signature: halimm
    @params: cloudapi.enterprise.addCampus(guid, '00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because there is no campus with that GUID
    """
    q.logger.log("         Adding non existing campus to the enterprise")
    assert_raises(xmlrpclib.Fault, cloudapi.enterprise.addCampus, guid, '00000000-0000-0000-0000-000000000000')