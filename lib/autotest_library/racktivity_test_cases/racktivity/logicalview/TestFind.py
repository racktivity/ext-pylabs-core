from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, lvGuid1, lvGuids
    ca = i.config.cloudApiConnection.find("main")
    lv1Guid = racktivity_test_library.logicalview.create('test_Logicalview1')
    lv2Guid = racktivity_test_library.logicalview.create('test_Logicalview2')
    lvGuids = (lv1Guid,lv2Guid)

def teardown():
    for guid in lvGuids:
        racktivity_test_library.logicalview.delete(guid)

def testFind_1():
    """
    @description: [0250401] Using find function to search for logicalview by its name
    @id: 0.25.04.01
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.find(name="test_Logicalview")['result']['guidlist']
    @expected_result: function should succeed and return the guid of the logicalview that starts with the name specified
    """
    q.logger.log("        Using find function to search by name")
    result = ca.logicalview.find(name="test_Logicalview")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in lvGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)
