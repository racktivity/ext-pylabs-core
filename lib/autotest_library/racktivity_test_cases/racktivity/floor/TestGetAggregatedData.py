from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, floorGuid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    floorGuid = racktivity_test_library.floor.create("test_floor1", dcguid)
     
def teardown():
    racktivity_test_library.floor.delete(floorGuid)

def testgetAggregatedData_1():
    """
    @description: [0.36.05.01] getting Aggregated data of a valid floor guid
    @id: 0.36.05.01
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.getAggregatedData(floorGuid ,'all')
    @expected_result: function should succeed
    """
    q.logger.log("        getting Aggregated data of a valid floor guid")
    ca.floor.getAggregatedData(floorGuid ,'all')

@raises(xmlrpclib.Fault)
def testgetAggregatedData_2():
    """
    @description: [0.36.05.02] getting Aggregated data of an invalid floor guid
    @id: 0.36.05.02
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.getAggregatedData('00000000-0000-0000-0000-000000000000' ,'all')
    @expected_result: function should fail because the rack guid is invalid
    """
    q.logger.log("        getting Aggregated data of an invalid floor guid")
    ca.floor.getAggregatedData('00000000-0000-0000-0000-000000000000' ,'all')
