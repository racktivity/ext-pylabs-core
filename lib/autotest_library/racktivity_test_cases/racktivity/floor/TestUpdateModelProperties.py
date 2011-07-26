from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, floorGuid1, dcguid
    data = getData()
    ca = data["ca"]
    dcguid = data["dcguid"]
    floorGuid1 = racktivity_test_library.floor.create("test_floor1", dcguid)

def teardown():
    racktivity_test_library.floor.delete(floorGuid1)

def testUpdate_1():
    """
    @description: [0.36.17.01] Updating floor name
    @id: 0.36.17.01
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.updateModelProperties(floorGuid1, name = "test_Floor_rename")
    @expected_result: floor name should be updated in the drp
    """
    q.logger.log("         Updating floor name")
    ca.floor.updateModelProperties(floorGuid1, name = "test_Floor_rename")
    floor = ca.floor.getObject(floorGuid1)
    assert_equal(floor.name, "test_Floor_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0.36.17.02] Updating floor description
    @id: 0.36.17.02
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.updateModelProperties(floorGuid1, description = "test_Floor_rename")
    @expected_result: floor description should be updated in the drp
    """
    q.logger.log("         Updating floor description")
    ca.floor.updateModelProperties(floorGuid1, description = "test_Floor_rename")
    floor = ca.floor.getObject(floorGuid1)
    assert_equal(floor.description, "test_Floor_rename", "Description attribute was not properly updated")

