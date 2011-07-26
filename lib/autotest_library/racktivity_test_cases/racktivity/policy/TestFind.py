from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, policyGuid1, policyGuids
    ca = i.config.cloudApiConnection.find("main")
    policy1Guid = racktivity_test_library.policy.create('test_Policy1')
    policy2Guid = racktivity_test_library.policy.create('test_Policy2')
    policyGuids = (policy1Guid,policy2Guid)

def teardown():
    for guid in policyGuids:
        racktivity_test_library.policy.delete(guid)

def testFind_1():
    """
    @description: [0190401] searching for policy by its name Using find function
    @id: 0190401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.policy.find(name="test_Policy")['result']['guidlist']
    @expected_result: function should return a valid policy guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.policy.find(name="test_Policy")['result']['guidlist']
    for guid in policyGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)
