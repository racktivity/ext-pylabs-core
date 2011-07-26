from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global cloudapi, guid
    cloudapi = i.config.cloudApiConnection.find("main")
    guid = racktivity_test_library.enterprise.create('test_enterprise1', 'test_enterprise1_description')

def teardown():
    racktivity_test_library.enterprise.delete(guid)

def testUpdate_1():
    """
    @description: [0.33.17.01] Updating enterprise name, description
    @id: 0.33.17.01
    @timestamp: 1298553343
    @signature: halimm
    @params: cloudapi.enterprise.updateModelProperties(guid, name = "test_enterprise_rename", description = "test_desc_Enterprise_rename")
    @expected_result: enterprise name and description should be updated
    """
    q.logger.log("         Updating enterprise name and description")
    cloudapi.enterprise.updateModelProperties(guid, name = "test_enterprise_rename", description = "test_desc_Enterprise_rename")
    ent1 = cloudapi.enterprise.getObject(guid)
    assert_equal(ent1.name, "test_enterprise_rename", "Name attribute was not properly updated")
    assert_equal(ent1.description, "test_desc_Enterprise_rename", "Description attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0.33.17.02] updating invalid enterprise
    @id: 0.33.17.04
    @timestamp: 1298553343
    @signature: mmagdy
    @params: cloudapi.enterprise.updateModelProperties('00000000-0000-0000-0000-000000000000', description = "test_enterprise_rename")
    @expected_result: update operation should fail with an exception
    """
    q.logger.log("         Updating enterprise description")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, cloudapi.enterprise.updateModelProperties, '00000000-0000-0000-0000-000000000000', description = "test_enterprise_rename")


