from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, rackGuid1, rackGuid2, pod1Guid
    data = getData()
    ca = p.api.action.racktivity
    rackGuid1 = data["rackguid1"]
    rackGuid2 = data["rackguid2"]
    roomGuid1=data["room1"]
    pod1Guid = racktivity_test_library.pod.create(roomGuid1, 'test_pod1', 'test_pod1_description', racks = [rackGuid1])

def teardown():
    racktivity_test_library.pod.delete(pod1Guid)

def testUpdate_1():
    """
    @description: [0.34.17.01] Updating pod name, alias and description
    @id: 0.34.17.01
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.updateModelProperties(pod1Guid, name = "test_pod_rename", description = "test_desc_pod_rename", alias = 'test_alias_pod_rename')
    @expected_result: pod name should be updated
    """
    q.logger.log("         Updating pod name, alias and description")
    ca.pod.updateModelProperties(pod1Guid, name = "test_pod_rename", description = "test_desc_pod_rename", alias = 'test_alias_pod_rename')
    pod1 = ca.pod.getObject(pod1Guid)
    assert_equal(pod1.name, "test_pod_rename", "Name attribute was not properly updated")
    assert_equal(pod1.alias, "test_alias_pod_rename", "Alias attribute was not properly updated")
    assert_equal(pod1.description, "test_desc_pod_rename", "Description attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0.34.17.02] Updating pod racks
    @id: 0.34.17.02
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.updateModelProperties(pod1Guid, description = "testing description")
    @expected_result: pod campuses should be updated
    """
    q.logger.log( "         Updating pod campuses")
    ca.pod.updateModelProperties(pod1Guid, description = "testing description")

def testUpdate_3():
    """
    @description: [0.34.17.03] updating invalid pod
    @id: 0.34.17.03
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.updateModelProperties('00000000-0000-0000-0000-000000000000', description = "test_pod_rename")
    @expected_result: update operation should fail with an exception
    """
    q.logger.log("         Updating pod description")
    assert_raises(xmlrpclib.Fault, ca.pod.updateModelProperties, '00000000-0000-0000-0000-000000000000', description = "test_pod_rename")


