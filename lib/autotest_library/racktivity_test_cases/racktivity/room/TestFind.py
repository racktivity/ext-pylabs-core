from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, dcguid, roomGuids
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    room1Guid = racktivity_test_library.room.create('test_Room1', dcguid, data['floorguid'])
    room2Guid = racktivity_test_library.room.create('test_Room2', dcguid, data['floorguid'])
    roomGuids = (room1Guid,room2Guid)

def teardown():
    for guid in roomGuids:
        racktivity_test_library.room.delete(guid)

def testFind_1():
    """
    @description: [0210401] searching for room by its name Using find function
    @id: 0210401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.find(name="test_Room")['result']['guidlist']
    @expected_result:function should return a valid room guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.room.find(name="test_Room*")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in roomGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

