from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, locGuid, dcGuids
    ca = p.api.action.racktivity
    locGuid = racktivity_test_library.location.create()
    dcGuids = list()
    for c in xrange(0,3):
       dcGuids.append(racktivity_test_library.datacenter.create("test_location%d"%c, locationguid=locGuid))
     

def teardown():
    racktivity_test_library.location.delete(locGuid)

def testListDatacenters_1():
    """
    @description: [0151001] Listing datacenters that is located in a specific location and validating the result to make sure that all datacenters that was created in this location are listed properly
    @id: 0151001
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.listDatacenters(locationGuid)['result']['guidlist']
    @expected_result: function should return list of datacenters in the location specified
    """
    q.logger.log("        Listing datacenters of a valid location guid")
    result = ca.location.listDatacenters(locGuid)['result']['guidlist']
    assert_equal(result.sort(), dcGuids.sort(), "the guids returned by listDatacenters() function are not correct")

@raises(xmlrpclib.Fault)
def testListDatacenters_2():
    """
    @description: [0151002] Listing datacenters of a location that doesn't exist
    @id: 0151002
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.listDatacenters('00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because location doesn't exist
    """
    q.logger.log("        Listing datacenters of an invalid location guid")
    result = ca.location.listDatacenters('00000000-0000-0000-0000-000000000000')
