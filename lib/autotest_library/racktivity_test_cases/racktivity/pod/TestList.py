from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, podGuids, roomguid
    data = getData()
    ca = data["ca"]
    roomguid = data["room1"]
    pod1Guid = racktivity_test_library.pod.create(roomguid, 'test_pod1')
    pod2Guid = racktivity_test_library.pod.create(roomguid, 'test_pod2')
    podGuids = (pod1Guid,pod2Guid)

def teardown():
    for podGuid in podGuids:
        ca.pod.delete(podGuid)

def testList_1():
    """
    @description: [0.34.11.01] his function will create some pods and for each created pod a list function is called with this pod's guid and make sure that the function succeed
    @id: 0.34.11.01
    @timestamp: 1298796257
    @signature: halimm
    @params: for guid in podGuids: ca.pod.list(guid)['result']['podinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each pod to make sure its listed")
    for guid in podGuids:
        result = ca.pod.list(guid)['result']['podinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0.34.11.02] this function will call the list function without any parameters and validate its output
    @id: 0.34.11.02
    @timestamp: 1298796257
    @signature: halimm
    @params: for info in ca.pod.list()['result']['podinfo']: assert(info['guid'] in podGuids)
    @expected_result: function should return a list that contains information about the pod I have created
    """
    q.logger.log("calling list once and make sure it only returns the pods I created")
    result = ca.pod.list()['result']['podinfo']
    for info in result:
        assert_true(info['guid'] in podGuids, "pod %s was returned by list() but I didn't create this pod"%info['guid'])
