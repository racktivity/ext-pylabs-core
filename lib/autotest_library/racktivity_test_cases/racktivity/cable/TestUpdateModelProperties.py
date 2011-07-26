from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, cableGuid1, roomguid
    data = getData()
    ca = data["ca"]
    cableGuid1 = racktivity_test_library.cable.create()

def teardown():
    racktivity_test_library.cable.delete(cableGuid1)

def testUpdate_1():
    """
    @description: [0031701]Updating cable name
    @id: 0031701
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.updateModelProperties(cableGuid1, name = "test_Cable_rename")
    @expected_result: cable name will change
    """
    q.logger.log("         Updating cable name")
    ca.cable.updateModelProperties(cableGuid1, name = "test_Cable_rename")
    cable = ca.cable.getObject(cableGuid1)
    assert_equal(cable.name, "test_Cable_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0031702]Updating cable description
    @id: 0031702
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.updateModelProperties(cableGuid1, description = "test_Cable_rename")
    @expected_result: cable type will change
    """
    q.logger.log("         Updating cable description")
    ca.cable.updateModelProperties(cableGuid1, description = "test_Cable_rename")
    cable = ca.cable.getObject(cableGuid1)
    assert_equal(cable.description, "test_Cable_rename", "Description attribute was not properly updated")

