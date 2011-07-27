from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
import time

def setup():
    global ca, policyGuid
    ca = p.api.action.racktivity
    policyGuid = racktivity_test_library.policy.create("test_policy")

def teardown():
    global policyGuid
    racktivity_test_library.policy.delete(policyGuid)

def testListToRun_1():
    """
    @description: [0191101] this function will try to list the policies that need to be run.
    @id: 0191101
    @timestamp: 1293360198
    @signature: mazmy
    @params: for guid in created Policy Guids: ca.policy.listToRun(guid)['result']['policyinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each policy to make sure it is listed")
    ca = p.api.action.racktivity
    #set the time to now
    ca.policy.updateModelProperties(policyGuid, lastrun=str(int(time.time())))
    result = ca.policy.listToRun()['result']['policyinfo']
    guids = map(lambda i: i['guid'], result)
    assert_false(policyGuid in guids, "Policy was listed although it should not be because it's not its time to run yet")
