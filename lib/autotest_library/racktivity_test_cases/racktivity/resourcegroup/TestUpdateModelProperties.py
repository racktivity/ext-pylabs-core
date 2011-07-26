from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, resgGuid1
    ca = i.config.cloudApiConnection.find("main")
    resgGuid1 = racktivity_test_library.resourcegroup.create("test_resourcegroup1")

def teardown():
    racktivity_test_library.resourcegroup.delete(resgGuid1)

def testUpdate_1():
    """
    @description: [2451701] trying to change resourcegroup's name and checking the drp to make sure its really changed
    @id: 2451701
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.updateModelProperties(resgGuid1, name = "test_Resourcegroup_rename")
    @expected_result: update operation should succeed and update the drp data
    """
    q.logger.log("         Updating resourcegroup name")
    ca.resourcegroup.updateModelProperties(resgGuid1, name = "test_Resourcegroup_rename")
    ca.resourcegroup.updateModelProperties(resgGuid1, description = "test_desc_Resourcegroup_rename")
    resg = ca.resourcegroup.getObject(resgGuid1)
    assert_equal(resg.name, "test_Resourcegroup_rename", "Name attribute was not properly updated")
    assert_equal(resg.description, "test_desc_Resourcegroup_rename", "Description attribute was not properly updated")

def testUpdate_2():
    """
    @description: [2451702] updating invalid resourcegroup
    @id: 2451702
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.updateModelProperties('00000000-0000-0000-0000-000000000000', description = "test_Resourcegroup_rename")
    @expected_result: update operation should fail with an exception
    """
    q.logger.log("         Updating resourcegroup description")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.resourcegroup.updateModelProperties, '00000000-0000-0000-0000-000000000000', description = "test_Resourcegroup_rename")
