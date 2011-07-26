from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, resgGuid, dvGuids
    ca = i.config.cloudApiConnection.find("main")
    resgGuid = racktivity_test_library.resourcegroup.create()
    dvGuids = list()
    data = getData()
    dvGuids = (data['devGuid1'], data['devGuid2'])
    for dvGuid in dvGuids:
        ca.resourcegroup.addDevice(resgGuid, dvGuid)

def teardown():
    racktivity_test_library.resourcegroup.delete(resgGuid)

def testRemoveDevice_1():
    """
    @description: [2451201] Adding new device to resource group
    @id: 2451201
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.listDevices(resourcegroupGuid)['result']['guidlist']
    @expected_result: function should succeed
    """
    
    q.logger.log("        Deleting devices from resource group")
    for devGuid in dvGuids:
        ca.resourcegroup.removeDevice(resgGuid, devGuid)
    result = ca.resourcegroup.listDevices(resgGuid)['result']['guidlist']
    assert_equal(len(result), 0, "according to listDevices() the devices were not deleted")

def testRemoveDevice_2():
    """
    @description: [2451202] Adding new device to invalid resource group
    @id: 2451202
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.listDevices('00000000-0000-0000-0000-000000000000')['result']['guidlist']
    @expected_result: function should fail
    """
    
    q.logger.log("        Adding invalid device guid to invalid resource group")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.resourcegroup.removeDevice, '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000')

