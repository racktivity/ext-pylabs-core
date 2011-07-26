from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, rackGuid1, rackGuid2, row1Guid
    data = getData()
    ca = data["ca"]
    rackGuid1 = data["rackguid1"]
    rackGuid2 = data["rackguid2"]
    pod1Guid = data["pod1"]
    row1Guid = racktivity_test_library.row.create(pod1Guid, 'test_row1')
    ca.row.addRack(row1Guid, rackGuid1)

def teardown():
    racktivity_test_library.row.delete(row1Guid)
    
def testRemoverack_1():
    """
    @description: [0.35.02.01] passing a non existing row GUID to the function 
    @id: 0.35.02.01
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.removeRack('00000000-0000-0000-0000-000000000000', rackGuid1)
    @expected_result: function should fail because there is no row with that GUID
    """
    q.logger.log("         Removing rack from non existing row")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.row.removeRack, '00000000-0000-0000-0000-000000000000', rackGuid1)

def testRemoverack_2():
    """
    @description: [0.35.02.02] Removing a rack from an row (passing valid: row and rack GUIDs)
    @id: 0.35.02.02
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.removerack(row1Guid, rackGuid1)
    @expected_result: function should remove the rack from the row racks 
    """
    q.logger.log("       Removing the rack from the row")
    ca.row.removeRack(row1Guid, rackGuid1)
    row1=ca.row.getObject(row1Guid)
    lenRacks = len(row1.racks)
    assert_equal(lenRacks, 0, "Expected no rack in the racks but got %d instead"%(lenRacks))

