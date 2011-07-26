from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, rowGuid, pod1Guid
    data = getData()
    ca = data["ca"]
    pod1Guid = data["pod1"]

def teardown():
    pass

def testDelete_1():
    """
    @description: [0.35.20.01] Deleting Previously created row
    @id: 0.35.20.01
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.delete(rowGuid)
    @expected_result:the row should be deleted
    """
    q.logger.log("    Deleting Previously created row")
    rowGuid = racktivity_test_library.row.create(pod1Guid, 'test_row1')
    ca.row.delete(rowGuid)
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.row.getObject, rowGuid)

def testDelete_2():
    """
    @description: [0.35.20.02] Deleting non existing row
    @id: 0.35.20.02
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the row doesn't exist
    """
    q.logger.log("    Deleting non existing row")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.row.delete, '00000000-0000-0000-0000-000000000000')


