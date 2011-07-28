from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, podGuids
    data = getData()
    ca = p.api.action.racktivity
    roomGuid1=data["room1"]
    pod1Guid = racktivity_test_library.pod.create(roomGuid1, 'test_pod1')
    pod2Guid = racktivity_test_library.pod.create(roomGuid1, 'test_pod2')
    podGuids = (pod1Guid,pod2Guid) 

def teardown():
    for guid in podGuids:
        racktivity_test_library.pod.delete(guid)

def testFind_1():
    """
    @description: [0.34.04.01] searching for pod by its name Using find function
    @id: 0.34.04.1
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.find(name="test_pod")['result']['guidlist']
    @expected_result: function should return a valid pod guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.pod.find(name="test_pod*")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in podGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

