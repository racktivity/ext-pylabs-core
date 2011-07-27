from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, resgGuid, dvGuids
    ca = p.api.action.racktivity
    resgGuid = racktivity_test_library.resourcegroup.create()
    dvGuids = list()
    data = getData()
    dvGuids = [data['devGuid1'], data['devGuid2']]

def teardown():
    racktivity_test_library.resourcegroup.delete(resgGuid)

def testAddDevice_1():
    """
    @description: [2451101] Adding new device to resource group
    @id: 2451101
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.listDevices(resourcegroupGuid)['result']['guidlist']
    @expected_result: function should succeed
    """
    
    q.logger.log("        Adding new device to resource group")
    for devGuid in dvGuids:
        ca.resourcegroup.addDevice(resgGuid, devGuid)
    result = ca.resourcegroup.listDevices(resgGuid)['result']['guidlist']
    assert_equal(result.sort(), dvGuids.sort(), "the guids returned by listDevices() function are not correct")

def testAddDevice_2():
    """
    @description: [2451102] Adding new device to invalid resource group
    @id: 2451102
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.listDevices('00000000-0000-0000-0000-000000000000')['result']['guidlist']
    @expected_result: function should fail
    """
    
    q.logger.log("        Adding invalid device guid to invalid resource group")
    assert_raises(xmlrpclib.Fault, ca.resourcegroup.addDevice, '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000')

