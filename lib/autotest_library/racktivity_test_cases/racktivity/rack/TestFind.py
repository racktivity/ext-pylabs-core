from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomguid, rackGuids
    data = getData()
    ca = p.api.action.racktivity
    roomguid = data["roomguid"]
    rack1Guid = racktivity_test_library.rack.create('test_Rack1', roomguid)
    rack2Guid = racktivity_test_library.rack.create('test_Rack2', roomguid)
    rackGuids = (rack1Guid,rack2Guid)

def teardown():
    for guid in rackGuids:
        racktivity_test_library.rack.delete(guid)

def testFind_1():
    """
    @description: [0190401] searching for rack by its name Using find function
    @id: 0190401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.find(name="test_Rack*")['result']['guidlist']
    @expected_result:function should return a valid rack guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.rack.find(name="test_Rack*")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in rackGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

