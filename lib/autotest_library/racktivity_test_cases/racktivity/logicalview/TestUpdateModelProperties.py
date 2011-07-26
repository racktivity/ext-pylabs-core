from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, lvGuid1
    ca = i.config.cloudApiConnection.find("main")
    lvGuid1 = racktivity_test_library.logicalview.create("test_logicalview1")

def teardown():
    racktivity_test_library.logicalview.delete(lvGuid1)

def testUpdate_1():
    """
    @description: [0251701] trying to change logicalview's name and checking the drp to make sure its really changed
    @id: 0.25.17.01
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.updateModelProperties(lvGuid1, name = "test_Logicalview_rename")
    @expected_result: update operation should succeed and update the drp data
    """
    q.logger.log("         Updating logicalview name")
    ca.logicalview.updateModelProperties(lvGuid1, name = "test_Logicalview_rename")
    ca.logicalview.updateModelProperties(lvGuid1, description = "test_desc_Logicalview_rename")
    lv = ca.logicalview.getObject(lvGuid1)
    assert_equal(lv.name, "test_Logicalview_rename", "Name attribute was not properly updated")
    assert_equal(lv.description, "test_desc_Logicalview_rename", "Description attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0251702] updating invalid logicalview
    @id: 0.25.17.02
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.updateModelProperties('00000000-0000-0000-0000-000000000000', description = "test_Logicalview_rename")
    @expected_result: update operation should fail with an exception
    """
    q.logger.log("         Updating logicalview description")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.logicalview.updateModelProperties, '00000000-0000-0000-0000-000000000000', description = "test_Logicalview_rename")
