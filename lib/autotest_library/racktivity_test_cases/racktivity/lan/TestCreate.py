from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, backplaneguid1
    data = getData()
    ca = p.api.action.racktivity
    backplaneguid1 = data["backplaneguid1"]

def teardown():
    racktivity_test_library.lan.delete(lan1Guid)
    racktivity_test_library.lan.delete(lan2Guid)

def testCreate_1():
    """
    @description: [0140201] Creating Lan by calling create function and passing only the non optional parameters
    @id: 0140201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, 'test_lan1', 'DYNAMIC', network = "10.0.0.0", netmask = "255.255.255.0")['result']['languid']
    @expected_result: function should create Lan and store it in the drp
    """
    global lan1Guid
    q.logger.log("         Creating lan")
    lan1Guid = ca.lan.create(backplaneguid1, 'test_lan1', 'DYNAMIC', network = "10.0.0.0", netmask = "255.255.255.0")['result']['languid']
    ok_(lan1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if lan exists")
    lan1 = ca.lan.getObject(lan1Guid)
    assert_equal(lan1.backplaneguid,backplaneguid1)
    assert_equal(lan1.name,'test_lan1')
    assert_equal(lan1.lantype,q.enumerators.lantype.DYNAMIC)

def testCreate_2():
    """
    @description: [0140202] Creating Lan by calling create function and passing all parameters (both optional and required parameters)
    @id: 0140202
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, 'test_lan2', 'STATIC', network="10.0.0.0", netmask="255.255.0.0", fromip="10.0.10.1", toip="10.0.200.1", gateway='10.0.0.1', dns='4.2.2.2', description='lan desc')['result']['languid']
    @expected_result: function should create Lan and store it in the drp
    """
    global lan2Guid
    q.logger.log("         Creating lan with optional params")
    lan2Guid = ca.lan.create(backplaneguid1, 'test_lan2', 'STATIC', network="10.0.0.0", netmask="255.255.0.0",
                             fromip="10.0.10.1", toip="10.0.200.1", gateway='10.0.0.1', dns=['4.2.2.2'], description='lan desc')['result']['languid']
    ok_(lan2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if lan exists")
    lan2 = ca.lan.getObject(lan2Guid)
    assert_equal(lan2.backplaneguid,backplaneguid1)
    assert_equal(lan2.name,'test_lan2')
    assert_equal(lan2.lantype,q.enumerators.lantype.STATIC)
    assert_equal(lan2.network, "10.0.0.0")
    assert_equal(lan2.netmask, "255.255.0.0")
    assert_equal(lan2.startip, "10.0.10.1")
    assert_equal(lan2.endip, "10.0.200.1")
    assert_equal(lan2.gateway, '10.0.0.1')
    assert_equal(len(lan2.dns), 1)
    assert_equal(lan2.dns[0].ip , '4.2.2.2')
    assert_equal(lan2.description, 'lan desc')

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0140203] Creating Lan by calling create function and passing a number as name instead of string
    @id: 0140203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, 7, 'DYNAMIC', network="10.0.0.0", netmask="255.255.255.0")
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating lan with Integer as name")
    ca.lan.create(backplaneguid1, 7, 'DYNAMIC', network="10.0.0.0", netmask="255.255.255.0")

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0140204] Creating lan with invalid/non existing backplane guid
    @id: 0140204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create('00000000-0000-0000-0000-000000000000', 'test_lan_failure', 'STATIC', network="10.0.0.0", netmask="255.255.255.0")
    @expected_result: function should fail because backplane guid doesn't exist
    """
    q.logger.log("         Creating lan with Integer as name")
    ca.lan.create('00000000-0000-0000-0000-000000000000', 'test_lan_failure', 'STATIC', network="10.0.0.0", netmask="255.255.255.0")

@raises(xmlrpclib.Fault)
def testCreate_5():
    """
    @description: [0140205] Creating lan with invalid lan type
    @id: 0140205
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, "test_lan_badtype", 'INVALID',  network="10.0.0.0", netmask="255.255.255.0")
    @expected_result: function should fail because an invalid lan type was passed as lan type parameter to the create function
    """
    q.logger.log("         Creating lan with invalid lan type")
    ca.lan.create(backplaneguid1, "test_lan_badtype", 'INVALID',  network="10.0.0.0", netmask="255.255.255.0")

@raises(xmlrpclib.Fault)
def testCreate_6():
    """
    @description: [0140206] Creating lan with invalid/malformed IPs
    @id: 0140206
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, "test_lan_invalid1", 'STATIC', network="10.0.0.0", netmask="255.255.255.0", fromip=':)', toip=':s')
    @expected_result: function should fail because IPs used for creating the lan are invalid
    """
    q.logger.log("         Creating lan with invalid IPs")
    ca.lan.create(backplaneguid1, "test_lan_invalid1", 'STATIC', network="10.0.0.0", netmask="255.255.255.0", fromip=':)', toip=':s')

@raises(xmlrpclib.Fault)
def testCreate_7():
    """
    @description: [0140207] Creating lan with start IP bigger than end IP
    @id: 0140207
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, "test_lan__invalid2", 'STATIC', network="10.0.0.0", netmask="255.255.255.0", fromip='10.0.0.30', toip='10.0.0.10')
    @expected_result: Function should fail because start ip should be less than end ip
    """
    q.logger.log("         Creating lan with invalid IPs")
    ca.lan.create(backplaneguid1, "test_lan__invalid2", 'STATIC', network="10.0.0.0", netmask="255.255.255.0", fromip='10.0.0.30', toip='10.0.0.10')

@raises(xmlrpclib.Fault)
def testCreate_8():
    """
    @description: [0140208] Creating lan with a valid network/netmask but a start/end ip outside the network range
    @id: 0140208
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, "test_lan__invalid2", 'STATIC', fromip='10.0.0.1', toip='10.0.0.10', network="192.168.20.1", netmask='255.255.255.0')
    @expected_result: function should fail because start/end ip should be within the network range
    """
    q.logger.log("         Creating lan with invalid IPs")
    ca.lan.create(backplaneguid1, "test_lan__invalid2", 'STATIC', fromip='10.0.0.1', toip='10.0.0.10', network="192.168.20.1", netmask='255.255.255.0')

@raises(xmlrpclib.Fault)
def testCreate_9():
    """
    @description: [0140209] Creating ipaddress with the same name by
    @id: 0140209
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.create(backplaneguid1, 'test_lan1', 'DYNAMIC', network = "10.0.0.0", netmask = "255.255.255.0")['result']['languid']
    @expected_result: function should fail because ipaddress name must be unique
    """
    q.logger.log("         Creating lan with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()


