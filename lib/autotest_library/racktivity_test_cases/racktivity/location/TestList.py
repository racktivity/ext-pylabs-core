from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, locGuids
    ca = p.api.action.racktivity
    locGuid1 = racktivity_test_library.location.create("test_location1")
    locGuid2 = racktivity_test_library.location.create("test_location2")
    locGuids = (locGuid1,locGuid2) 

def teardown():
    for guid in locGuids:
        racktivity_test_library.location.delete(guid)

def testList_1():
    """
    @description: [0151101] this function will create some locations and for each created location a list function is called with this location's guid and make sure that the function succeed
    @id: 0151101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdLocationGuids: result = ca.location.list(guid)['result']['locationinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each location to make sure its listed")
    for guid in locGuids:
        result = ca.location.list(guid)['result']['locationinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0151102] this function will call the list function without any parameters and validate its output
    @id: 0151102
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for info in ca.location.list()['result']['locationinfo']: assert(info['guid'] in createdlocationGuids)
    @expected_result: function should return a list that contains information about the location I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.location.list()['result']['locationinfo']
    for info in result:
        ok_(info['guid'] in locGuids, "location %s was returned by list() but I didn't create this location"%info['guid'])

