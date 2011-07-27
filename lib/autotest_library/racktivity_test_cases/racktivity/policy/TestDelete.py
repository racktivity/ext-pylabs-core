from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, policyGuid
    ca = p.api.action.racktivity
    policyGuid = racktivity_test_library.policy.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [0190301] Deleting Previously created policy
    @id: 0190301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.policy.delete(policyGuid)
    @expected_result:the policy should be deleted
    """
    q.logger.log("    Deleting Previously created policy")
    ca.policy.delete(policyGuid)
    assert_raises(xmlrpclib.Fault, ca.policy.getObject, policyGuid)


@raises(xmlrpclib.Fault)
def testDelete_2():
    """
    @description: [0190302] Deleting non existing policy
    @id: 0190302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.policy.delete('00000000-0000-0000-0000-000000000000')
    @expected_result:the policy should be deleted
    """
    q.logger.log("    Deleting non existing policy")
    ca.policy.delete('00000000-0000-0000-0000-000000000000')

