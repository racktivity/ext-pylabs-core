from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, backplaneGuid1, roomguid
    data = getData()
    ca = p.api.action.racktivity
    backplaneGuid1 = racktivity_test_library.backplane.create()

def teardown():
    racktivity_test_library.backplane.delete(backplaneGuid1)

def testUpdate_1():
    """
    @description: [0021701] Updating backplane name
    @id: 0021701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.updateModelProperties(backplaneGuid, name = "test_Backplane_rename")
    @expected_result: backplane name will change
    """
    q.logger.log("         Updating backplane name")
    ca.backplane.updateModelProperties(backplaneGuid1, name = "test_Backplane_rename")
    backplane = ca.backplane.getObject(backplaneGuid1)
    assert_equal(backplane.name, "test_Backplane_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0021702] Updating backplane description
    @id: 0021702
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.updateModelProperties(backplaneGuid1, description = "test_Backplane_rename")
    @expected_result: backplane description will change
    """
    q.logger.log("         Updating backplane description")
    ca.backplane.updateModelProperties(backplaneGuid1, description = "test_Backplane_rename")
    backplane = ca.backplane.getObject(backplaneGuid1)
    assert_equal(backplane.description, "test_Backplane_rename", "Description attribute was not properly updated")

def testUpdate_3():
    """
    @description: [0021703] Updating backplane type
    @id: 0021703
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.updateModelProperties(backplaneGuid1, backplanetype = "ETHERNET")
    @expected_result: backplane type will change
    """
    q.logger.log("         Updating backplane type") 
    ca.backplane.updateModelProperties(backplaneGuid1, backplanetype = "ETHERNET")
    backplane = ca.backplane.getObject(backplaneGuid1)
    assert_equal(backplane.backplanetype, "ETHERNET", "Type attribute was not properly updated")
    ca.backplane.updateModelProperties(backplaneGuid1, backplanetype = "INFINIBAND")
    backplane = ca.backplane.getObject(backplaneGuid1)
    assert_equal(backplane.backplanetype, "INFINIBAND" , "Type attribute was not properly updated")

