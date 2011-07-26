from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, ipGuid1
    ca = i.config.cloudApiConnection.find("main")
    ipGuid1 = racktivity_test_library.ipaddress.create("test_lpaddress1")

def teardown():
    racktivity_test_library.ipaddress.delete(ipGuid1)

def testUpdate_1():
    """
    @description: [0121701] Updating ipaddress name
    @id: 0121701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.updateModelProperties(ipGuid1, name = "test_Ipaddress_rename")
    @expected_result: ipaddress name should be updated
    """
    q.logger.log("         Updating ipaddress name")
    ca.ipaddress.updateModelProperties(ipGuid1, name = "test_Ipaddress_rename")
    ip = ca.ipaddress.getObject(ipGuid1)
    assert_equal(ip.name, "test_Ipaddress_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0121702] Updating ipaddress description
    @id: 0121702
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.updateModelProperties(ipGuid1, description = "test_Ipaddress_rename")
    @expected_result: ipaddress description should be updated
    """
    q.logger.log("         Updating ipaddress description")
    ca.ipaddress.updateModelProperties(ipGuid1, description = "test_Ipaddress_rename")
    ip = ca.ipaddress.getObject(ipGuid1)
    assert_equal(ip.description, "test_Ipaddress_rename", "Description attribute was not properly updated")

