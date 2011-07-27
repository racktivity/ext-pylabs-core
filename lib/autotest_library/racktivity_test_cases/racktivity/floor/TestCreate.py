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
    racktivity_test_library.floor.delete(floor1Guid)
    racktivity_test_library.floor.delete(floor2Guid)

def testCreate_1():
    """
    @description: [0.36.02.01] Creating Floor by calling create function and passing only the non optional parameters
    @id: 0.36.02.01
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.create('test_floor1', dcguid)['result']['floorguid']
    @expected_result: function should create Floor and store it in the drp
    """
    global floor1Guid
    q.logger.log("         Creating Floor")
    floor1Guid = ca.floor.create('test_floor1', 0, dcguid)['result']['floorguid']
    ok_(floor1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if floor exists")
    floor1 = ca.floor.getObject(floor1Guid)
    assert_equal(floor1.name,'test_floor1')
    assert_equal(floor1.datacenterguid,dcguid)

def testCreate_2():
    """
    @description: [0.36.02.02] Creating Floor by calling create function and passing all parameters (both optional and required parameters)
    @id: 0.36.02.02
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.create('test_floor2', dcguid, 'test_floor2_description', "test_floor2_floor", "test_floor2_alias")['result']['floorguid']
    @expected_result: function should create Floor and store it in the drp
    """
    global floor2Guid
    q.logger.log("         Creating Floor with optional params")
    floor2Guid = ca.floor.create('test_floor2', 0, dcguid, "test_floor2_alias", 'test_floor2_description', "test_floor2_floor tags")['result']['floorguid']
    ok_(floor2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if floor exists")
    floor1 = ca.floor.getObject(floor2Guid)
    assert_equal(floor1.name,'test_floor2')
    assert_equal(floor1.datacenterguid,dcguid)
    assert_equal(floor1.description,'test_floor2_description')
    assert_equal(floor1.floor, 0)
    assert_equal(floor1.alias,'test_floor2_alias')

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0.36.02.03] Creating Floor by calling create function and passing a number as name instead of string
    @id: 0.36.02.03
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.create(7, dcguid)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating floor with Integer as name")
    ca.floor.create(7, 0, dcguid)

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0.36.02.04] calling create function with an invalid datacenter guid as a parameter
    @id: 0.36.02.04
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.create("test_floor_negative", '00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because the datacenter guid is not valid
    """
    q.logger.log("         Creating floor with invalid datacenter guid")
    ca.floor.create("test_floor_negative", 0, '00000000-0000-0000-0000-000000000000')

@raises(xmlrpclib.Fault)
def testCreate_5():
    """
    @description: [0.36.02.05] Creating floor with a name that already exists
    @id: 0.36.02.05
    @timestamp: 1298883563
    @signature: mazmy
    @params: ca.floor.create('test_floor1', dcguid)['result']['floorguid']
    @expected_result: function should fail because floor name must be unique
    """
    q.logger.log("         Creating floor with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

