from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, dcguid, floorGuids
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    floor1Guid = racktivity_test_library.floor.create('test_Floor1', dcguid)
    floor2Guid = racktivity_test_library.floor.create('test_Floor2', dcguid)
    floorGuids = (floor1Guid,floor2Guid)

def teardown():
    for guid in floorGuids:
        racktivity_test_library.floor.delete(guid)

def testFind_1():
    """
    @description: [0.36.04.01] searching for floor by its name Using find function
    @id: 0.36.04.01
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.find(name="test_Floor")['result']['guidlist']
    @expected_result:function should return a valid floor guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.floor.find(name="test_Floor")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in floorGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

