from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, lanGuid1
    data = getData()
    ca = p.api.action.racktivity
    lanGuid1 = racktivity_test_library.lan.create("test_lan1", data["backplaneguid1"])

def teardown():
    racktivity_test_library.lan.delete(lanGuid1)

def testUpdate_1():
    """
    @description: [0141701] Updating lan name
    @id: 0141701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.updateModelProperties(lanGuid1, name = "test_Lan_rename")
    @expected_result:new name should be saved in the drp 
    """
    q.logger.log("         Updating lan name")
    ca.lan.updateModelProperties(lanGuid1, name = "test_Lan_rename")
    lan = ca.lan.getObject(lanGuid1)
    assert_equal(lan.name, "test_Lan_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0141702] Updating lan description
    @id: 0141702
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.updateModelProperties(lanGuid1, description = "test_Lan_rename")
    @expected_result:new description should be saved in the drp
    """
    q.logger.log("         Updating lan description")
    ca.lan.updateModelProperties(lanGuid1, description = "test_Lan_rename")
    lan = ca.lan.getObject(lanGuid1)
    assert_equal(lan.description, "test_Lan_rename", "Description attribute was not properly updated")

