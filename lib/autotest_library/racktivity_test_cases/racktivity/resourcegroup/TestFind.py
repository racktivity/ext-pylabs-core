from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, resgGuid1, resgGuids
    ca = i.config.cloudApiConnection.find("main")
    resg1Guid = racktivity_test_library.resourcegroup.create('test_Resourcegroup1')
    resg2Guid = racktivity_test_library.resourcegroup.create('test_Resourcegroup2')
    resgGuids = (resg1Guid,resg2Guid)

def teardown():
    for guid in resgGuids:
        racktivity_test_library.resourcegroup.delete(guid)

def testFind_1():
    """
    @description: [2450401] Using find function to search for resourcegroup by its name
    @id: 2450401
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.find(name="test_Resourcegroup")['result']['guidlist']
    @expected_result: function should succeed and return the guid of the resourcegroup that starts with the name specified
    """
    q.logger.log("        Using find function to search by name")
    result = ca.resourcegroup.find(name="test_Resourcegroup")['result']['guidlist']
    for guid in resgGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)
