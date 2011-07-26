from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, rackGuid1, pod1Guid
    data = getData()
    ca = data["ca"]
    rackGuid1 = data["rackguid1"]
    pod1Guid = racktivity_test_library.pod.create(data["room1"], 'test_pod1')
    ca.pod.addRack(pod1Guid, rackGuid1)
    
def teardown():
    racktivity_test_library.pod.delete(pod1Guid)
    
def testRemoverack_1():
    """
    @description: [0.34.21.01] passing a non existing pod GUID to the function 
    @id: 0.34.21.01
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.removeRack('00000000-0000-0000-0000-000000000000', rackGuid1)
    @expected_result: function should fail because there is no pod with that GUID
    """
    q.logger.log("         Removing rack from non existing pod")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.pod.removeRack, '00000000-0000-0000-0000-000000000000', rackGuid1)

def testRemoverack_2():
    """
    @description:[0.34.21.02] Removing a rack from an pod (passing valid: pod and rack GUIDs)
    @id: 0.34.21.02
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.removerack(pod1Guid, rackGuid1)
    @expected_result: function should remove the rack from the pod racks 
    """
    q.logger.log("       Removing the rack from the pod")
    ca.pod.removeRack(pod1Guid, rackGuid1)
    pod1=ca.pod.getObject(pod1Guid)
    racks=pod1.racks
    assert_equal(len(racks), 0, "Expected no rack in the racks but got %d instead"%(len(racks)))

