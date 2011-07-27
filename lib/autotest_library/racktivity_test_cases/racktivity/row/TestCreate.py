from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, rackGuid1, roomGuid1, pod1Guid
    data = getData()
    ca = p.api.action.racktivity
    pod1Guid = data["pod1"]
    rackGuid1 = data["rackguid1"]
    roomGuid1 = data["room1"]

def teardown():
    ca.row.removeRack(row2Guid, rackGuid1)
    racktivity_test_library.row.delete(row1Guid)
    racktivity_test_library.row.delete(row2Guid)

def testCreate_1():
    """
    @description: [0.35.02.01] Creating row by calling create function and passing only the non optional parameters
    @id: 0.35.02.01
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.create()['result']['rowguid']
    @expected_result: function should create row and store it in the drp
    """
    global row1Guid
    q.logger.log("         Creating row")
    row1Guid = ca.row.create(name = "test_row", pod=pod1Guid, room=roomGuid1)['result']['rowguid']
    q.logger.log("         Checking if row exists")
    ok_(row1Guid, "Empty guid returned from create function")
    
def testCreate_2():
    """
    @description: [0.35.02.02] Creating row by calling create function and passing all parameters (both optional and required parameters)
    @id: 0.35.02.02
    @timestamp: 1298812206
    @signature: halimm
    @params:ca.row.create(name='test_row_optional', description='Test Description', alias='Test Alias', room=roomGuid1, racks=[rackGuid1])['result']['rowguid']
    @expected_result: function should create row and store it in the drp
    """
    global row2Guid
    q.logger.log("         Creating row with optional params")
    row2Guid = ca.row.create(name='test_row_optional', description='Test Description', alias='Test Alias', pod=pod1Guid, room=roomGuid1, racks=[rackGuid1])['result']['rowguid']
    ok_(row2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if row exists")
    row2 = ca.row.getObject(row2Guid)
    ok_(row2.name == 'test_row_optional', "Name of resource group is different than the name given to it during creation")

def testCreate_3():
    """
    @description: [0.35.02.03] Creating row by calling create function and passing a number as name instead of string
    @id: 0.35.02.03
    @timestamp: 1298812206
    @signature: halimm
    @params:ca.row.create(name=7)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating row with Integer as name")
    assert_raises(xmlrpclib.Fault, ca.row.create,name = 7)

def testCreate_4():
    """
    @description: [0.35.02.04] Creating row with Non existing rackguid
    @id: 0.35.02.04
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.create('test_row_err' , racks=['00000000-0000-0000-0000-000000000000'])
    @expected_result: function should fail because locationguid is invalid/doesn't exists
    """
    q.logger.log("         Creating row with Non existing rackguid")
    assert_raises(xmlrpclib.Fault, ca.row.create, racks=['00000000-0000-0000-0000-000000000000'])

def testCreate_5():
    """
    @description: [0.35.02.05] Creating row with a name that already exists
    @id: 0.35.02.05
    @timestamp: 1298812206
    @signature: halimm
    @params:ca.row.create('test_row_optional')['result']['rowguid']
    @expected_result: function should fail because row name must be unique
    """
    q.logger.log("         Creating row with the same name by calling testCreate_Positive() again")
    assert_raises(xmlrpclib.Fault, testCreate_2)


