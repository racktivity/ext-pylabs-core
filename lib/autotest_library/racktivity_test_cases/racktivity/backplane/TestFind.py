from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomguid, backplaneGuids
    data = getData()
    ca = p.api.action.racktivity
    backplane1Guid = racktivity_test_library.backplane.create('test_Backplane1')
    backplane2Guid = racktivity_test_library.backplane.create('test_Backplane2')
    backplaneGuids = (backplane1Guid,backplane2Guid)

def teardown():
    for guid in backplaneGuids:
        racktivity_test_library.backplane.delete(guid)

def testFind_1():
    """
    @description: [0020401] searching for backplane by its name Using find function
    @id: 0020401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.find(name="test_Backplane")['result']['guidlist']
    @expected_result: function should return a valid backplane guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.backplane.find(name="test_Backplane*")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in backplaneGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

