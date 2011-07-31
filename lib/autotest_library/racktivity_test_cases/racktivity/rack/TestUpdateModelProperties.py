from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, rackGuid1, roomguid
    data = getData()
    ca = p.api.action.racktivity
    roomguid = data["roomguid"]
    rackGuid1 = racktivity_test_library.rack.create("test_rack1", roomguid)

def teardown():
    racktivity_test_library.rack.delete(rackGuid1)

def testUpdate_1():
    """
    @description: [0191701] Updating rack name
    @id: 0191701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.updateModelProperties(rackGuid1, name = "test_Rack_rename")
    @expected_result: rack name should be updated in the drp
    """
    q.logger.log("         Updating rack name")
    ca.rack.updateModelProperties(rackGuid1, name = "test_Rack_rename")
    rack = ca.rack.getObject(rackGuid1)
    assert_equal(rack.name, "test_Rack_rename", "Name attribute was not properly updated")
    rack1 = ca.rack.getObject(rackGuid1)

def testUpdate_2():
    """
    @description: [0191702] Updating rack description
    @id: 0191702
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.updateModelProperties(rackGuid1, description = "test_Rack_rename")
    @expected_result: rack description should be updated in the drp
    """
    q.logger.log("         Updating rack description")
    ca.rack.updateModelProperties(rackGuid1, description = "test_Rack_rename")
    rack = ca.rack.getObject(rackGuid1)
    assert_equal(rack.description, "test_Rack_rename", "Description attribute was not properly updated")

