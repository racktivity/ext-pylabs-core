from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, languid1
    data = getData()
    ca = data['ca']

def teardown():
    racktivity_test_library.policy.delete(policy1Guid)
    racktivity_test_library.policy.delete(policy2Guid)

def testCreate_1():
    """
    @description: [0190201] Creating Policy by calling create function and passing only the non optional parameters
    @id: 0190201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.policy.create("test_policy1", "racktivity", "backup", None, 10)['result']['policyguid']
    @expected_result: function should create Policy and store it in the drp
    """
    global policy1Guid
    q.logger.log("         Creating policy")
    policy1Guid = ca.policy.create("test_policy1", "racktivity", "backup", None, 10)['result']['policyguid']
    ok_(policy1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if policy exists")
    policy1 = ca.policy.getObject(policy1Guid)
    assert_equal(policy1.name, "test_policy1")
    assert_equal(policy1.rootobjecttype, "racktivity")
    assert_equal(policy1.rootobjectaction, "backup")

def testCreate_2():
    """
    @description: [0190202] Creating Policy by calling create function and passing all parameters (both optional and required parameters)
    @id: 0190202
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.policy.create('test_policy2', .........
    @expected_result: function should create Policy and store it in the drp
    """
    global policy2Guid
    q.logger.log("         Creating policy")
    policy2Guid = ca.policy.create("test_policy2", "racktivity", "backup", None, 10,
                                   runbetween='[("00:00", "24:00")]', runnotbetween='[("00:00", "24:00")]',
                                   policyparams='{}', description='TheyPolicy')['result']['policyguid']
    ok_(policy2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if policy exists")
    policy2 = ca.policy.getObject(policy2Guid)
    assert_equal(policy2.name, "test_policy2")
    assert_equal(policy2.rootobjecttype, "racktivity")
    assert_equal(policy2.rootobjectaction, "backup")
    assert_equal(policy2.runbetween, '[("00:00", "24:00")]')
    assert_equal(policy2.runnotbetween, '[("00:00", "24:00")]')
    assert_equal(policy2.policyparams, "{}")
    assert_equal(policy2.description, "TheyPolicy")

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_3():
    """
    @description: [0190203] Creating Policy by calling create function and passing an invalid guid as rootobject guid
    @id: 0190203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.policy.create(7, "10.1.0.1")
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating policy with Integer as name")
    ca.policy.create("test_policy1", "racktivity", "backup", 'InvalidGuid', 10)
