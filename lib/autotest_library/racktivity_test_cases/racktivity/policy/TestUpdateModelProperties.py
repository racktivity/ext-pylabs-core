from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, policyGuid1
    ca = p.api.action.racktivity
    policyGuid1 = racktivity_test_library.policy.create()

def teardown():
    racktivity_test_library.policy.delete(policyGuid1)

def testUpdate_1():
    """
    @description: [0191701] Updating policy properties
    @id: 0191701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.policy.updateModelProperties(policyGuid1, name = "test_Policy_rename")
    @expected_result: policy name should be updated
    """
    q.logger.log("         Updating policy name")
    ca.policy.updateModelProperties(policyGuid1, name = "test_policy",
                                   interval = 10.0, runbetween='[("00:00", "24:00")]',
                                   runnotbetween='[("00:00", "24:00")]', policyparams='{}', description='TheyPolicy')
    policy = ca.policy.getObject(policyGuid1)
    assert_equal(policy.name, "test_policy")
    assert_equal(policy.runbetween, '[("00:00", "24:00")]')
    assert_equal(policy.runnotbetween, '[("00:00", "24:00")]')
    assert_equal(policy.policyparams, "{}")
    assert_equal(policy.description, "TheyPolicy")
