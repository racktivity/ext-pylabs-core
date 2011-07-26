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
    dvGuids = [data['devGuid1'], data['devGuid2']]
    for dvGuid in dvGuids:
        ca.resourcegroup.addDevice(resgGuid, dvGuid)

def teardown():
    racktivity_test_library.resourcegroup.delete(resgGuid)

def testListDevices_1():
    """
    @description: [2451001] Listing devices that is located in a specific resourcegroup and validating the result to make sure that all devices that was created in this resourcegroup are listed properly
    @id: 2451001
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.listDevices(resourcegroupGuid)['result']['guidlist']
    @expected_result: function should return list of devices in the resourcegroup specified
    """
    q.logger.log("        Listing devices of a valid resourcegroup guid")
    result = ca.resourcegroup.listDevices(resgGuid)['result']['guidlist']
    assert_equal(result.sort(), dvGuids.sort(), "the guids returned by listDevices() function are not correct")

def testListDevices_2():
    """
    @description: [2451002] Listing devices of a resourcegroup that doesn't exist
    @id: 2451002
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.listDevices('00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because resourcegroup doesn't exist
    """
    q.logger.log("        Listing devices of an invalid resourcegroup guid")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.resourcegroup.listDevices, '00000000-0000-0000-0000-000000000000')
