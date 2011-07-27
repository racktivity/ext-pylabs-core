from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomguid, lanGuids
    data = getData()
    ca = p.api.action.racktivity
    lan1Guid = racktivity_test_library.lan.create('test_Lan1', data["backplaneguid1"])
    lan2Guid = racktivity_test_library.lan.create('test_Lan2', data["backplaneguid1"])
    lanGuids = (lan1Guid,lan2Guid)

def teardown():
    for guid in lanGuids:
        racktivity_test_library.lan.delete(guid)

def testFind_1():
    """
    @description: [0140401] searching for lan by its name Using find function
    @id: 0140401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdLanGuids: assert(guid in ca.lan.find(name="test_Lan")['result']['guidlist']) 
    @expected_result: function should succeed and return a valid lan guid
    """
    q.logger.log("        Using find function to search by name")
    result = ca.lan.find(name="test_Lan")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in lanGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

