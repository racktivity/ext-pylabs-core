from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

NAME = 'test_enterprise1'
def setup():
    global cloudapi, guid
    cloudapi = i.config.cloudApiConnection.find("main")
    guid = racktivity_test_library.enterprise.create(NAME)

def teardown():
    racktivity_test_library.enterprise.delete(guid)

def testFind_1():
    """
    @description: [0.33.04.01] searching for enterprise by its name Using find function
    @id: 0.33.04.01
    @timestamp: 1298553343
    @signature: halimm
    @params: cloudapi.enterprise.find(name="test_enterprise")['result']['guidlist']
    @expected_result: function should return a valid enterprise guid 
    """
    q.logger.log("        Using find function to search by name")
    result = cloudapi.enterprise.find(name=NAME)['result']['guidlist']
    ok_(guid in result, "Guid %s was not returned by find()" % guid)

