from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, pod1Guid, rackGuid1, rackGuid2
    data = getData()
    ca = p.api.action.racktivity
    rackGuid1 = data["rackguid1"]
    rackGuid2 = data["rackguid2"]
    
    pod1Guid = racktivity_test_library.pod.create(data["room1"], 'test_pod1')

def teardown():
    ca.pod.removeRack(pod1Guid, rackGuid1)
    ca.pod.removeRack(pod1Guid, rackGuid2)
    racktivity_test_library.pod.delete(pod1Guid)
    
def testAddrack_1():
    """
    @description: [0.33.20.01] passing a non existing pod GUID to the function 
    @id: 0.33.20.01
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.addRack('00000000-0000-0000-0000-000000000000', rackGuid1)
    @expected_result: function should fail because there is no pod with that GUID
    """
    q.logger.log("         Adding rack to non existing pod")
    assert_raises(xmlrpclib.Fault, ca.pod.addRack, '00000000-0000-0000-0000-000000000000', rackGuid1)

def testAddrack_2():
    """
    @description: [0.33.20.02] passing a non existing rack GUID to the function
    @id: 0.33.20.02
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.addRack(pod1Guid, '00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because there is no rack with that GUID
    """
    q.logger.log("         Adding non existing rack to the pod")
    assert_raises(xmlrpclib.Fault, ca.pod.addRack, pod1Guid, '00000000-0000-0000-0000-000000000000')

def testAddrack_3():
    """
    @description: [0.33.20.03] Adding a rack to an pod and passing valid: pod and rack GUIDs
    @id: 0.33.20.03
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.addRack(pod1Guid, rackGuid1)
    @expected_result: function should add the rack to the pod racks 
    """
    q.logger.log("       adding the rack to the pod")
    ca.pod.addRack(pod1Guid, rackGuid1)
    pod1=ca.pod.getObject(pod1Guid)
    racks=pod1.racks
    assert_equal(len(racks), 1, "Expected a single rack in the racks but got %d instead"%(len(racks)))

def testAddrack_4():
    """
    @description: [0.33.20.04] Adding a second rack to a pod (passing valid: pod and rack GUIDs)
    @id: 0.33.20.04
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.addRack(pod1Guid, rackGuid2)
    @expected_result: function should append the rack to the pod racks 
    """
    q.logger.log("       adding the rack to the pod")
    ca.pod.addRack(pod1Guid, rackGuid2)
    pod1=ca.pod.getObject(pod1Guid)
    racks=pod1.racks
    assert_equal(len(racks), 2, "Expected 2 racks in the racks list but got %d instead"%(len(racks)))
    
def testAddrack_5():
    """
    @description: [0.33.20.05] adding a rack to the pod which already has the same rack in its racks
    @id: 0.33.20.05
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.addRack(pod1Guid, rackGuid1)
    @expected_result: function should fail because rackguid already exists in the racks list
    """
    q.logger.log("         adding an already existing rack to the racks list")
    assert_raises(xmlrpclib.Fault, ca.pod.addRack, pod1Guid, rackGuid1)


