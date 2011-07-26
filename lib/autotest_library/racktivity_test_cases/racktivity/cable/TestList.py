from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, cableGuids, roomguid
    data = getData()
    ca = data["ca"]
    cableGuid1 = racktivity_test_library.cable.create("test_cable1")
    cableGuid2 = racktivity_test_library.cable.create("test_cable2")
    cableGuids = (cableGuid1,cableGuid2) 

def teardown():
    for guid in cableGuids:
        racktivity_test_library.cable.delete(guid)

def testList_1():
    """
    @description: [0031101] this function will create some cables and for each created cable a list function is called with this cable's guid and make sure that the function succeed
    @id: 0031101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdCablesGuids: ca.cable.list(guid)['result']['cableinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each cable to make sure its listed")
    for guid in cableGuids:
        result = ca.cable.list(guid)['result']['cableinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['cableguid'], guid, "list returned guid %s expected %s"%(result[0]['cableguid'], guid))

def testList_2():
    """
    @description : [0031102] this function will call the list function without any parameters and validate its output
    @id: 0031102
    @timestamp: 1293360198
    @signature: mmagdy
    @params : ca.cable.list()
    @expected_result: function should return a list that contains information about the cables I have created
    """
    q.logger.log("make sure that list() only returns the cables I created")
    result = ca.cable.list()['result']['cableinfo']
    for info in result:
        ok_(info['cableguid'] in cableGuids, "cable %s was returned by list() but I didn't create this cable"%info['cableguid'])
