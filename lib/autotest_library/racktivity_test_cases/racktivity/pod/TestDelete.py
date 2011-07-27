from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, podGuid, roomGuid1
    data = getData()
    ca = p.api.action.racktivity
    roomGuid1=data["room1"]
    podGuid = racktivity_test_library.pod.create(roomGuid1, 'test_pod1')

def teardown():
    pass

def testDelete_1():
    """
    @description: [0.34.03.01] Deleting Previously created pod
    @id: 0.34.03.01
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.delete(podGuid)
    @expected_result:the pod should be deleted
    """
    q.logger.log("    Deleting Previously created pod")
    ca.pod.delete(podGuid)
    assert_raises(xmlrpclib.Fault, ca.pod.getObject, podGuid)

def testDelete_2():
    """
    @description: [0.34.03.02] Deleting non existing pod
    @id: 0.34.03.02
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the pod doesn't exist
    """
    q.logger.log("    Deleting non existing pod")
    assert_raises(xmlrpclib.Fault, ca.pod.delete, '00000000-0000-0000-0000-000000000000')


