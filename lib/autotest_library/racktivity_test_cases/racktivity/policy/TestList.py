from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, policyGuids
    ca = p.api.action.racktivity
    policyGuid1 = racktivity_test_library.policy.create("test_policy1")
    policyGuid2 = racktivity_test_library.policy.create("test_policy2")
    policyGuids = (policyGuid1,policyGuid2) 

def teardown():
    for guid in policyGuids:
        racktivity_test_library.policy.delete(guid)

def testList_1():
    """
    @description: [0191101] this function will create some policies and for each created policy a list function is called with this policy's guid and make sure that the function succeed
    @id: 0191101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in created Policy Guids: ca.policy.list(guid)['result']['policyinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each policy to make sure its listed")
    for guid in policyGuids:
        result = ca.policy.list(guid)['result']['policyinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0191102] this function will call the list function without any parameters and validate its output
    @id: 0191102
    @timestamp: 1293360198
    @signature: mmagdy
    @params:    for info in result: assert(info['guid'] in policyGuids)
    @expected_result: function should return a list that contains information about the policy I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.policy.list()['result']['policyinfo']
    guids = map(lambda i: i['guid'], result)
    for guid in policyGuids:
        ok_(guid in guids, "Can't find policy '%s' in the policyes returned by list()" % guid)
