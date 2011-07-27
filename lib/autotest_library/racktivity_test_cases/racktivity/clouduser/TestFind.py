from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, locGuid1, locGuids
    ca = p.api.action.racktivity
    loc1Guid = racktivity_test_library.clouduser.create('test_user1')
    loc2Guid = racktivity_test_library.clouduser.create('test_user2')
    locGuids = (loc1Guid,loc2Guid)

def teardown():
    for guid in locGuids:
        racktivity_test_library.clouduser.delete(guid)

def testFind_1():
    """
    @description: [0050401] searching for clouduser by its name Using find function
    @id: 0050401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.clouduser.find(login="test_user*")['result']['guidlist']
    @expected_result: function should return a valid clouduser guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.clouduser.find(login="test_user")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in locGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

