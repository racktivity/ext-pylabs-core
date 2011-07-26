from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, languid1
    data = getData()
    languid1 = data["lanGuid1"]
    ca = data['ca']

def teardown():
    racktivity_test_library.ipaddress.delete(ip1Guid)
    racktivity_test_library.ipaddress.delete(ip2Guid)

def testCreate_1():
    """
    @description: [0120201] Creating Ipaddress by calling create function and passing only the non optional parameters
    @id: 0120201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.create('test_ipaddress1', "192.168.20.1")['result']['ipaddressguid']
    @expected_result: function should create Ipaddress and store it in the drp
    """
    global ip1Guid
    q.logger.log("         Creating ipaddress")
    ip1Guid = ca.ipaddress.create('test_ipaddress1', "192.168.20.1")['result']['ipaddressguid']
    ok_(ip1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if ipaddress exists")
    ip1 = ca.ipaddress.getObject(ip1Guid)
    assert_equal(ip1.name, "test_ipaddress1")
    assert_equal(ip1.address, "192.168.20.1")

def testCreate_2():
    """
    @description: [0120202] Creating Ipaddress by calling create function and passing all parameters (both optional and required parameters)
    @id: 0120202
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.create('test_ipaddress2', "192.168.20.2", "ip description", "255.255.255.255", True, "DHCP", "IPV4", languid1, True)['result']['ipaddressguid']
    @expected_result: function should create Ipaddress and store it in the drp
    """
    global ip2Guid
    q.logger.log("         Creating ipaddress")
    ip2Guid = ca.ipaddress.create('test_ipaddress2', "192.168.20.2", "ip description", "255.255.255.255", True, "DHCP", "IPV4", languid1, True)['result']['ipaddressguid']
    ok_(ip2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if ipaddress exists")
    ip2 = ca.ipaddress.getObject(ip2Guid)
    assert_equal(ip2.name, "test_ipaddress2")
    assert_equal(ip2.address, "192.168.20.2")
    assert_equal(ip2.description, "ip description")
    assert_equal(ip2.netmask, "255.255.255.255")
    assert_equal(ip2.block, True)
    assert_equal(ip2.iptype, q.enumerators.iptype.DHCP)
    assert_equal(ip2.ipversion, q.enumerators.ipversion.IPV4)
    assert_equal(ip2.languid, languid1)
    assert_equal(ip2.virtual, True)

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_3():
    """
    @description: [0120203] Creating Ipaddress by calling create function and passing a number as name instead of string
    @id: 0120203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.create(7, "10.1.0.1")
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating ipaddress with Integer as name")
    ca.ipaddress.create(7, "10.1.0.1")

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_4():
    """
    @description: [0120204] Creating Ipaddress by calling create function and passing a number as name instead of string
    @id: 0120204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.create("test_ipaddress_invalid_1", 100)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating ipaddress with Integer as an ip")
    ca.ipaddress.create("test_ipaddress_invalid_1", 100)

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_5():
    """
    @description: [0120205] Creating ipaddress with Integer as an ip
    @id: 0120205
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.create("test_ipaddress_invalid_2", "265.255.0.2")
    @expected_result: function should fail because integers are not allowed as IP
    """
    q.logger.log("         Creating ipaddress with Integer as an ip")
    ca.ipaddress.create("test_ipaddress_invalid_2", "265.255.0.2")

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_6():
    """
    @description: [0120206] Creating ipaddress with a name that already exists
    @id: 0120206
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.create('test_ipaddress1', "192.168.20.1")
    @expected_result: function should fail because ipaddress name must be unique
    """
    q.logger.log("         Creating ipaddress with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

