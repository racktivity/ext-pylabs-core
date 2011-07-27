from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]

def teardown():
    racktivity_test_library.feed.delete(feed1Guid)
    racktivity_test_library.feed.delete(feed2Guid)

def testCreate_1():
    """
    @description: [0230201] Creating Feed by calling create function and passing only the non optional parameters
    @id: 0230201
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.create('test_feed1', dcguid, "COAL")['result']['feedguid']
    @expected_result: function should create Feed and store it in the drp
    """
    global feed1Guid
    q.logger.log("         Creating Feed")
    feed1Guid = ca.feed.create('test_feed1', "COAL", dcguid)['result']['feedguid']
    ok_(feed1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if feed exists")
    feed1 = ca.feed.getObject(feed1Guid)
    assert_equal(feed1.name,'test_feed1')
    assert_equal(feed1.datacenterguid,dcguid)
    assert_equal(feed1.productiontype,q.enumerators.feedProductionType.COAL)

def testCreate_2():
    """
    @description: [0230202] Creating Feed by calling create function and passing all parameters (both optional and required parameters)
    @id: 0230202
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.create('test_feed2', "GAS", description= 'test_feed2_description')['result']['feedguid']
    @expected_result: function should create Feed and store it in the drp
    """
    global feed2Guid
    q.logger.log("         Creating Feed with optional params")
    feed2Guid = ca.feed.create('test_feed2', "GAS", dcguid, description= 'test_feed2_description')['result']['feedguid']
    ok_(feed2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if feed exists")
    feed1 = ca.feed.getObject(feed2Guid)
    assert_equal(feed1.name,'test_feed2')
    assert_equal(feed1.datacenterguid,dcguid)
    assert_equal(feed1.productiontype,q.enumerators.feedProductionType.GAS)
    assert_equal(feed1.description,'test_feed2_description')

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0230203] Creating Feed by calling create function and passing a number as name instead of string
    @id: 0230203
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.create(7, dcguid)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating feed with Integer as name")
    ca.feed.create(7, "GAS", dcguid)

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0230204] calling create function with an invalid datacenter guid as a parameter
    @id: 0230204
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.create("test_feed_negative", '00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because the datacenter guid is not valid
    """
    q.logger.log("         Creating feed with invalid datacenter guid")
    ca.feed.create("test_feed_negative", "GAS", '00000000-0000-0000-0000-000000000000')

@raises(xmlrpclib.Fault)
def testCreate_5():
    """
    @description: [0230205] Creating feed with a name that already exists
    @id: 0230205
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.create('test_feed1', dcguid)['result']['feedguid']
    @expected_result: function should fail because feed name must be unique
    """
    q.logger.log("         Creating feed with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

