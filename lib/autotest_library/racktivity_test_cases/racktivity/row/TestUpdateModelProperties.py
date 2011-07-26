from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, row1Guid
    data = getData()
    ca = data["ca"]
    pod1Guid = data["pod1"]
    row1Guid = racktivity_test_library.row.create(pod1Guid, 'test_row1', 'test_row1_description')

def teardown():
    racktivity_test_library.row.delete(row1Guid)

def testUpdate_1():
    """
    @description: [0.35.17.01] Updating row name, alias and description
    @id: 0.35.17.01
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.updateModelProperties(row1Guid, name = "test_row_rename", description = "test_desc_row_rename", alias = 'test_alias_row_rename')
    @expected_result: row name should be updated
    """
    q.logger.log("         Updating row name, alias and description")
    ca.row.updateModelProperties(row1Guid, name = "test_row_rename", description = "test_desc_row_rename", alias = 'test_alias_row_rename')
    row1 = ca.row.getObject(row1Guid)
    assert_equal(row1.name, "test_row_rename", "Name attribute was not properly updated")
    assert_equal(row1.alias, "test_alias_row_rename", "Alias attribute was not properly updated")
    assert_equal(row1.description, "test_desc_row_rename", "Description attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0.35.17.02] updating invalid row
    @id: 0.35.17.02
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.updateModelProperties('00000000-0000-0000-0000-000000000000', description = "test_row_rename")
    @expected_result: update operation should fail with an exception
    """
    q.logger.log("         Updating row description")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.row.updateModelProperties, '00000000-0000-0000-0000-000000000000', description = "test_row_rename")


