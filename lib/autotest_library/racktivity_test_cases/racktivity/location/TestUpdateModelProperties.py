from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, locGuid1
    ca = p.api.action.racktivity
    locGuid1 = racktivity_test_library.location.create("test_location1")

def teardown():
    racktivity_test_library.location.delete(locGuid1)

def testUpdate_1():
    """
    @description: [0151701] trying to change location's name and checking the drp to make sure its really changed
    @id: 0151701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.updateModelProperties(locGuid1, name = "test_Location_rename")
    @expected_result: update operation should succeed and update the drp data
    """
    q.logger.log("         Updating location name")
    ca.location.updateModelProperties(locGuid1, name = "test_Location_rename")
    loc = ca.location.getObject(locGuid1)
    assert_equal(loc.name, "test_Location_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0151702] trying to change location's description and checking the drp to make sure its really changed
    @id: 0151702
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.updateModelProperties(locGuid1, description = "test_Location_rename")
    @expected_result: update operation should succeed and update the drp data
    """
    q.logger.log("         Updating location description")
    ca.location.updateModelProperties(locGuid1, description = "test_Location_rename")
    loc = ca.location.getObject(locGuid1)
    assert_equal(loc.description, "test_Location_rename", "Description attribute was not properly updated")

