from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomGuid,dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    roomGuid = racktivity_test_library.room.create("test_room1", dcguid, data['floorguid'])

def teardown():
    pass

def testDelete_1():
    """
    @description: [0210301] Deleting Previously created room
    @id: 0210301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.delete(roomGuid)
    @expected_result: the room should be deleted
    """
    q.logger.log("    Deleting Previously created room")
    room1 = ca.room.getObject(roomGuid)
    ca.room.delete(roomGuid)
    assert_raises(xmlrpclib.Fault, ca.room.getObject, roomGuid)
    racktivity_test_library.ui.doUITest(room1.datacenterguid, "DELETE", value=room1.name)
    ok_(racktivity_test_library.ui.getResult(room1.name))

@raises(xmlrpclib.Fault)
def testDelete_2():
    """
    @description: [0210302] Deleting non existing room
    @id: 0210302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.delete('00000000-0000-0000-0000-000000000000')
    @expected_result:the room should be deleted
    """
    q.logger.log("    Deleting non existing room")
    ca.room.delete('00000000-0000-0000-0000-000000000000')

