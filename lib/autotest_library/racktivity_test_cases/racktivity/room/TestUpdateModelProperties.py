from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomGuid1, dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    roomGuid1 = racktivity_test_library.room.create("test_room1", dcguid, data['floorguid'])

def teardown():
    racktivity_test_library.room.delete(roomGuid1)

def testUpdate_1():
    """
    @description: [0211701] Updating room name
    @id: 0211701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.updateModelProperties(roomGuid1, name = "test_Room_rename")
    @expected_result: room name should be updated in the drp
    """
    q.logger.log("         Updating room name")
    ca.room.updateModelProperties(roomGuid1, name = "test_Room_rename")
    room = ca.room.getObject(roomGuid1)
    assert_equal(room.name, "test_Room_rename", "Name attribute was not properly updated")


def testUpdate_2():
    """
    @description: [0211702] Updating room description
    @id: 0211702
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.updateModelProperties(roomGuid1, description = "test_Room_rename")
    @expected_result: room description should be updated in the drp
    """
    q.logger.log("         Updating room description")
    ca.room.updateModelProperties(roomGuid1, description = "test_Room_rename")
    room = ca.room.getObject(roomGuid1)
    assert_equal(room.description, "test_Room_rename", "Description attribute was not properly updated")

