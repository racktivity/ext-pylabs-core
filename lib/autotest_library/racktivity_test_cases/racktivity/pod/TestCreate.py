from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, roomGuid1
    data = getData()
    ca = p.api.action.racktivity
    roomGuid1=data["room1"]

def teardown():
    racktivity_test_library.pod.delete(pod1Guid)
    racktivity_test_library.pod.delete(pod2Guid)

def testCreate_1():
    """
    @description: [0.34.02.01] Creating pod by calling create function and passing only the non optional parameters
    @id: 0.34.02.01
    @timestamp: 1298796257
    @signature: halimm
    @params: ca.pod.create()['result']['podguid']
    @expected_result: function should create pod and store it in the drp
    """
    global pod1Guid
    q.logger.log("         Creating pod")
    pod1Guid = ca.pod.create(name='test_pod', room=roomGuid1)['result']['podguid']
    q.logger.log("         Checking if pod exists")
    ok_(pod1Guid, "Empty guid returned from create function")
    
def testCreate_2():
    """
    @description: [0.34.02.02] Creating pod by calling create function and passing all parameters (both optional and required parameters)
    @id: 0.34.02.02
    @timestamp: 1298796257
    @signature: halimm
    @params:ca.pod.create(name='test_pod_optional', description='Test Description', alias='Test Alias', room=roomGuid1)['result']['podguid']
    @expected_result: function should create pod and store it in the drp
    """
    global pod2Guid
    q.logger.log("         Creating pod with optional params")
    pod2Guid = ca.pod.create(name='test_pod_optional', description='Test Description', alias='Test Alias', room=roomGuid1)['result']['podguid']
    ok_(pod2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if pod exists")
    pod2 = ca.pod.getObject(pod2Guid)
    ok_(pod2.name == 'test_pod_optional', "Name of resource group is different than the name given to it during creation")

def testCreate_3():
    """
    @description: [0.34.02.03] Creating pod by calling create function and passing a number as name instead of string
    @id: 0.34.02.03
    @timestamp: 1298796257
    @signature: halimm
    @params:ca.pod.create(name=7)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating pod with Integer as name")
    assert_raises(xmlrpclib.Fault, ca.pod.create,name= 7)

def testCreate_4():
    """
    @description: [0.34.02.04] Creating pod with a name that already exists
    @id: 0.34.02.05
    @timestamp: 1298796257
    @signature: halimm
    @params:ca.pod.create('test_pod_optional')['result']['podguid']
    @expected_result: function should fail because pod name must be unique
    """
    q.logger.log("         Creating pod with the same name by calling testCreate_Positive() again")
    assert_raises(xmlrpclib.Fault, testCreate_2)


