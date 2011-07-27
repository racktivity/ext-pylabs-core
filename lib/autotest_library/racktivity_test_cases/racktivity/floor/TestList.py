from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, floorGuids, dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    floorGuid1 = racktivity_test_library.floor.create("test_floor1", dcguid)
    floorGuid2 = racktivity_test_library.floor.create("test_floor2", dcguid)
    floorGuids = (floorGuid1,floorGuid2) 

def teardown():
    for guid in floorGuids:
        racktivity_test_library.floor.delete(guid)

def testList_1():
    """
    @description: [0.36.11.01] this function will create some floors and for each created floor a list function is called with this floor's guid and make sure that the function succeed
    @id: 0.36.11.01
    @timestamp: 1298883563
    @signature: mazmy
    @params: for guid in createdFloorGuids: floor.list(guid)['result']['floorinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each floor to make sure its listed")
    for guid in floorGuids:
        result = ca.floor.list(guid)['result']['floorinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0.36.11.02] this function will call the floor list function without any parameters and validate its output
    @id: 0.36.11.02
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.list()['result']['floorinfo']
    @expected_result: function should return a list that contains information about the floor I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.floor.list()['result']['floorinfo']
    guids = map(lambda i: i['guid'], result)
    for guid in floorGuids:
        ok_(guid in guids, "Can't find floor  %s in list" % guid)
        
