from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, locGuid1, locGuids
    ca = p.api.action.racktivity
    loc1Guid = racktivity_test_library.location.create('test_Location1')
    loc2Guid = racktivity_test_library.location.create('test_Location2')
    locGuids = (loc1Guid,loc2Guid)

def teardown():
    for guid in locGuids:
        racktivity_test_library.location.delete(guid)

def testFind_1():
    """
    @description: [0150401] Using find function to search for location by its name
    @id: 0150401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.find(name="test_Location")['result']['guidlist']
    @expected_result: function should succeed and return the guid of the location that starts with the name specified
    """
    q.logger.log("        Using find function to search by name")
    result = ca.location.find(name="test_Location")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in locGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

