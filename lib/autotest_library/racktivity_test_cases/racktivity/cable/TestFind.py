from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, roomguid, cableGuids
    data = getData()
    ca = p.api.action.racktivity
    cable1Guid = racktivity_test_library.cable.create('test_Cable1')
    cable2Guid = racktivity_test_library.cable.create('test_Cable2')
    cableGuids = (cable1Guid,cable2Guid)

def teardown():
    for guid in cableGuids:
        racktivity_test_library.cable.delete(guid)

def testFind_1():
    """
    @description: [0030401] searching for cable by its name Using find function
    @id: 0030401
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.find(name="test_Cable")['result']['guidlist']
    @expected_result: function should return a valid cable guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.cable.find(name="test_Cable")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in cableGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

