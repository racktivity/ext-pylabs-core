from nose.tools import *
from pylabs import q, i
import racktivity_test_library
from . import getCloudapi, getDatacenterGuid, getRoomGuid, getRackGuid, getMeteringDeviceGuid, getLogicalViewGuid, getRequest

def testDataExportForHypervisor_1():
    """
    @description: [0.40.02.01] Test Data Export For Hypervisor (using the meteringdevice guid)
    @id: 0.40.02.01
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForHypervisor(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForHypervisor(getMeteringDeviceGuid(), request = getRequest())
    assert_true(data['result']['export'])
    
    
def testDataExportForHypervisor_2():
    """
    @description: [0.40.02.02] Test Data Export For Hypervisor (using the rack guid)
    @id: 0.40.02.02
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForHypervisor(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForHypervisor(getRackGuid(), request = getRequest())
    assert_true(data['result']['export'])

def testDataExportForHypervisor_3():
    """
    @description: [0.40.02.03] Test Data Export For Hypervisor (using the room guid)
    @id: 0.40.02.03
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForHypervisor(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForHypervisor(getRoomGuid(), request = getRequest())
    assert_true(data['result']['export'])
    
def testDataExportForHypervisor_4():
    """
    @description: [0.40.02.04] Test Data Export For Hypervisor (using the datacenter guid)
    @id: 0.40.02.04
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForHypervisor(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForHypervisor(getDatacenterGuid(), request = getRequest())
    assert_true(data['result']['export'])

def testDataExportForHypervisor_5():
    """
    @description: [0.40.02.05] Test Data Export For Hypervisor (using the logicalview guid)
    @id: 0.40.02.05
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForHypervisor(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForHypervisor(getLogicalViewGuid(), request = getRequest())
    assert_true(data['result']['export'])

