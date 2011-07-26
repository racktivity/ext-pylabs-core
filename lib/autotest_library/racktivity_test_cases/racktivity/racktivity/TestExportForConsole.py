from nose.tools import *
from pymonkey import q, i
import racktivity_test_library
from . import getCloudapi, getDatacenterGuid, getRoomGuid, getRackGuid, getMeteringDeviceGuid, getLogicalViewGuid, getRequest

def testDataExportForConsole_1():
    """
    @description: [0.40.01.01] Test Data Export For Console (using the meteringdevice guid)
    @id: 0.40.01.01
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForConsole(guid)
    @expected_result: An XML string.
    """
    
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForConsole(getMeteringDeviceGuid(), request = getRequest())
    assert_true(data['result']['export'])
    
    
def testDataExportForConsole_2():
    """
    @description: [0.40.01.02] Test Data Export For Console (using the rack guid)
    @id: 0.40.01.02
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForConsole(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForConsole(getRackGuid(), request = getRequest())
    assert_true(data['result']['export'])

def testDataExportForConsole_3():
    """
    @description: [0.40.01.03] Test Data Export For Console (using the room guid)
    @id: 0.40.01.03
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForConsole(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForConsole(getRoomGuid(), request = getRequest())
    assert_true(data['result']['export'])
    
def testDataExportForConsole_4():
    """
    @description: [0.40.01.04] Test Data Export For Console (using the datacenter guid)
    @id: 0.40.01.04
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForConsole(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForConsole(getDatacenterGuid(), request = getRequest())
    assert_true(data['result']['export'])

def testDataExportForConsole_5():
    """
    @description: [0.40.01.05] Test Data Export For Console (using the logicalview guid)
    @id: 0.40.01.05
    @timestamp: 1293360198
    @signature: mazmy
    @params: cloudapi.racktivity.exportForConsole(guid)
    @expected_result: An XML string.
    """
    cloudapi = getCloudapi()
    
    data = cloudapi.racktivity.exportForConsole(getLogicalViewGuid(), request = getRequest())
    assert_true(data['result']['export'])

