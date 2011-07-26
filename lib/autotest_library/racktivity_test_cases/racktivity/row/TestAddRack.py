from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, rackGuid1, rackGuid2, row1Guid
    data = getData()
    ca = data["ca"]
    pod1Guid = data["pod1"]
    rackGuid1 = data["rackguid1"]
    rackGuid2 = data["rackguid2"]

    row1Guid = racktivity_test_library.row.create(pod1Guid, 'test_row1')

def teardown():
    ca.row.removeRack(row1Guid, rackGuid1)
    ca.row.removeRack(row1Guid, rackGuid2)
    racktivity_test_library.row.delete(row1Guid)
    
def testAddrack_1():
    """
    @description: [0.35.20.01] passing a non existing row GUID to the function 
    @id: 0.35.20.01
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.addRack('00000000-0000-0000-0000-000000000000', rackGuid1)
    @expected_result: function should fail because there is no row with that GUID
    """
    q.logger.log("         Adding rack to non existing row")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.row.addRack, '00000000-0000-0000-0000-000000000000', rackGuid1)

def testAddrack_2():
    """
    @description: [0.35.20.02] passing a non existing rack GUID to the function
    @id: 0.35.20.02
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.addRack(row1Guid, '00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because there is no rack with that GUID
    """
    q.logger.log("         Adding non existing rack to the row")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.row.addRack, row1Guid, '00000000-0000-0000-0000-000000000000')
    #in case the rack has been added to the row racks
    ca.row.removeRack(row1Guid, '00000000-0000-0000-0000-000000000000')

def testAddrack_3():
    """
    @description: [0.35.20.03] Adding a rack to an row and passing valid: row and rack GUIDs
    @id: 0.35.20.03
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.addRack(row1Guid, rackGuid1)
    @expected_result: function should add the rack to the row racks 
    """
    q.logger.log("       adding the rack to the row")
    ca.row.addRack(row1Guid, rackGuid1)
    row1=ca.row.getObject(row1Guid)
    racks=row1.racks
    assert_equal(len(racks), 1, "Expected a single rack in the racks but got %d instead"%(len(racks)))

def testAddrack_4():
    """
    @description: [0.35.20.04] Adding a second rack to an row (passing valid: row and rack GUIDs)
    @id: 0.35.20.04
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.addRack(row1Guid, rackGuid2)
    @expected_result: function should append the rack to the row racks 
    """
    q.logger.log("       adding the rack to the row")
    ca.row.addRack(row1Guid, rackGuid2)
    row1=ca.row.getObject(row1Guid)
    racks=row1.racks
    assert_equal(len(racks), 2, "Expected 2 racks in the racks list but got %d instead"%(len(racks)))
    
def testAddrack_5():
    """
    @description: [0.35.20.05] adding a rack to the row which already has the same rack in its racks
    @id: 0.35.20.05
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.addRack(row1Guid, rackGuid1)
    @expected_result: function should fail because rackguid already exists in the racks list
    """
    q.logger.log("         adding an already existing rack to the racks list")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.row.addRack, row1Guid, rackGuid1)


