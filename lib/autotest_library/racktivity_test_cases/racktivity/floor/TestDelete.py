from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, floorGuid,dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    floorGuid = racktivity_test_library.floor.create("test_floor1", dcguid)

def teardown():
    pass

def testDelete_1():
    """
    @description: [0.36.03.01] Deleting Previously created floor
    @id: 0.36.03.01
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.delete(floorGuid)
    @expected_result: the floor should be deleted
    """
    q.logger.log("    Deleting Previously created floor")
    floor1 = ca.floor.getObject(floorGuid)
    ca.floor.delete(floorGuid)
    assert_raises(xmlrpclib.Fault, ca.floor.getObject, floorGuid)

@raises(xmlrpclib.Fault)
def testDelete_2():
    """
    @description: [0.36.03.02] Deleting non existing floor
    @id: 0.36.03.02
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.delete('00000000-0000-0000-0000-000000000000')
    @expected_result:the floor should be deleted
    """
    q.logger.log("    Deleting non existing floor")
    ca.floor.delete('00000000-0000-0000-0000-000000000000')

