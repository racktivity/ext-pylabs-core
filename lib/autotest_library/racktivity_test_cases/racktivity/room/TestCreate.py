from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, dcguid, floorguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    floorguid = data['floorguid']

def teardown():
    racktivity_test_library.room.delete(room1Guid)
    racktivity_test_library.room.delete(room2Guid)

def testCreate_1():
    """
    @description: [0210201] Creating Room by calling create function and passing only the non optional parameters
    @id: 0210201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.create('test_room1', dcguid, floor=floorguid)['result']['roomguid']
    @expected_result: function should create Room and store it in the drp
    """
    global room1Guid
    q.logger.log("         Creating Room")
    room1Guid = ca.room.create('test_room1', dcguid, floorguid=floorguid)['result']['roomguid']
    ok_(room1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if room exists")
    room1 = ca.room.getObject(room1Guid)
    assert_equal(room1.name,'test_room1')
    assert_equal(room1.datacenterguid,dcguid)

def testCreate_2():
    """
    @description: [0210202] Creating Room by calling create function and passing all parameters (both optional and required parameters)
    @id: 0210202
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.create('test_room2', dcguid, description='test_room2_description', floor=floorguid, alias="test_room2_alias")['result']['roomguid']
    @expected_result: function should create Room and store it in the drp
    """
    global room2Guid, floorguid
    q.logger.log("         Creating Room with optional params")
    room2Guid = ca.room.create('test_room2', dcguid, description='test_room2_description', floorguid=floorguid, alias="test_room2_alias")['result']['roomguid']
    ok_(room2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if room exists")
    room1 = ca.room.getObject(room2Guid)
    assert_equal(room1.name,'test_room2')
    assert_equal(room1.datacenterguid,dcguid)
    assert_equal(room1.description,'test_room2_description')
    assert_equal(room1.floorguid, floorguid)
    assert_equal(room1.alias,'test_room2_alias')

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0210203] Creating Room by calling create function and passing a number as name instead of string
    @id: 0210203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.create(7, dcguid, floor=floorguid)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating room with Integer as name")
    ca.room.create(7, dcguid, floorguid=floorguid)

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0210204] calling create function with an invalid datacenter guid as a parameter
    @id: 0210204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.create("test_room_negative", '00000000-0000-0000-0000-000000000000', floor=floorguid)
    @expected_result: function should fail because the datacenter guid is not valid
    """
    q.logger.log("         Creating room with invalid datacenter guid")
    ca.room.create("test_room_negative", '00000000-0000-0000-0000-000000000000', floor=floorguid)

@raises(xmlrpclib.Fault)
def testCreate_5():
    """
    @description: [0210205] Creating room with a name that already exists
    @id: 0210205
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.room.create('test_room1', dcguid, floor=floorguid)['result']['roomguid']
    @expected_result: function should fail because room name must be unique
    """
    q.logger.log("         Creating room with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

