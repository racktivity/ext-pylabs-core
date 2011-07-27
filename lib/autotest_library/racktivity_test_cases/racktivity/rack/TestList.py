from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, rackGuids, roomguid
    data = getData()
    ca = p.api.action.racktivity
    roomguid = data["roomguid"]
    rackGuid1 = racktivity_test_library.rack.create("test_rack1", roomguid)
    rackGuid2 = racktivity_test_library.rack.create("test_rack2", roomguid)
    rackGuids = (rackGuid1,rackGuid2) 

def teardown():
    for guid in rackGuids:
        racktivity_test_library.rack.delete(guid)

def testList_1():
    """
    @description: [0191101] this function will create some racks and for each created rack a list function is called with this rack's guid and make sure that the function succeed
    @id: 0191101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdRackGuids: ca.rack.list(guid)['result']['rackinfo']
    @expected_result: function should succeed
    """
    q.logger.log("        calling list for each rack to make sure its listed")
    for guid in rackGuids:
        result = ca.rack.list(guid)['result']['rackinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0191102] this function will call the list function without any parameters and validate its output
    @id: 0191102
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for info in ca.rack.list()['result']['rackinfo']: assert(info['guid'] in rackGuids)
    @expected_result: function should return a list that contains information about the rack I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.rack.list()['result']['rackinfo']
    guids = map(lambda i: i['guid'], result)
    for guid in rackGuids:
        ok_(guid in guids, "Rack '%s' not returned by list()" % guid)
