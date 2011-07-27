from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomGuids, dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    roomGuid1 = racktivity_test_library.room.create("test_room1", dcguid, data['floorguid'])
    roomGuid2 = racktivity_test_library.room.create("test_room2", dcguid, data['floorguid'])
    roomGuids = (roomGuid1,roomGuid2) 

def teardown():
    for guid in roomGuids:
        racktivity_test_library.room.delete(guid)

def testList_1():
    """
    @description: [0211101] this function will create some rooms and for each created room a list function is called with this room's guid and make sure that the function succeed
    @id: 0211101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdRoomGuids: room.list(guid)['result']['roominfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each room to make sure its listed")
    for guid in roomGuids:
        result = ca.room.list(guid)['result']['roominfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0211102] this function will call the list function without any parameters and validate its output
    @id: 0211102
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.list()['result']['roominfo']
    @expected_result: function should return a list that contains information about the room I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.room.list()['result']['roominfo']
    for info in result:
        ok_(info['guid'] in roomGuids, "room %s was returned by list() but I didn't create this room"%info['guid'])
