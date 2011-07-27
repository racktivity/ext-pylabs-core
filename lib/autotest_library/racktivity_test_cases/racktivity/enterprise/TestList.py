from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

NAME = 'test_enterprise1'
def setup():
    global cloudapi, guid
    cloudapi = p.api.action.racktivity
    guid = racktivity_test_library.enterprise.create(NAME)

def teardown():
    racktivity_test_library.enterprise.delete(guid)

def testList_1():
    """
    @description: [0.33.11.01] List enterprise object
    @id: 0.33.11.01
    @timestamp: 1298553343
    @signature: halimm
    @params: for guid in enterpriseGuids: ca.enterprise.list(guid)['result']['enterpriseinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each enterprise to make sure its listed")
    result = cloudapi.enterprise.list()['result']['enterpriseinfo']
    guids = map(lambda i: i['guid'], result)
    ok_(guid in guids, "Can't find enterprise '%s' in the guids returned by list()" % guid)
    
def testList_1():
    """
    @description: [0.33.11.01] List enterprise object with a wrong enterprise guid
    @id: 0.33.11.02
    @timestamp: 1298553343
    @signature: halimm
    @params: for guid in enterpriseGuids: ca.enterprise.list(guid)['result']['enterpriseinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each enterprise to make sure its listed")
    result = cloudapi.enterprise.list("00000000-0000-0000-0000-000000000000")['result']['enterpriseinfo']
    assert_false(result, "List returned data with wrong guid")
