from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomGuid
    data = getData()
    ca = p.api.action.racktivity
    roomGuid = racktivity_test_library.room.create("test_room1", data["dcguid"], data['floorguid'])
     
def teardown():
    racktivity_test_library.room.delete(roomGuid)

def testgetAggregatedData_1():
    """
    @description: [0210501] getting Aggregated data of a valid room guid
    @id: 0210501
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.getAggregatedData(roomGuid ,'all')
    @expected_result: function should succeed
    """
    q.logger.log("        getting Aggregated data of a valid room guid")
    ca.room.getAggregatedData(roomGuid ,'all')

@raises(xmlrpclib.Fault)
def testgetAggregatedData_2():
    """
    @description: [0210502] getting Aggregated data of an invalid room guid
    @id: 0210502
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.getAggregatedData('00000000-0000-0000-0000-000000000000' ,'all')
    @expected_result: function should fail because the rack guid is invalid
    """
    q.logger.log("        getting Aggregated data of an invalid room guid")
    ca.room.getAggregatedData('00000000-0000-0000-0000-000000000000' ,'all')
