from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, rackGuid
    data = getData()
    ca = data["ca"]
    roomguid = data["roomguid"]
    rackGuid = racktivity_test_library.rack.create("test_rack1", roomguid)
     
def teardown():
    racktivity_test_library.rack.delete(rackGuid)

def testgetAggregatedData_1():
    """
    @description: [0190501] getting the Aggregated data of a valid rack guid
    @id: 0190501
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.getAggregatedData(rackGuid ,'all')
    @expected_result: function should succeed
    """
    q.logger.log("        getting Aggregated data of a valid rack guid")
    ca.rack.getAggregatedData(rackGuid ,'all')

@raises(cloud_api_client.Exceptions.CloudApiException)
def testgetAggregatedData_2():
    """
    @description: [0190502] getting Aggregated data of an invalid rack guid
    @id: 0190502
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.getAggregatedData('00000000-0000-0000-0000-000000000000' ,'all')
    @expected_result:function should fail because the rack guid is invalid
    """
    q.logger.log("        getting Aggregated data of an invalid rack guid")
    ca.rack.getAggregatedData('00000000-0000-0000-0000-000000000000' ,'all')
