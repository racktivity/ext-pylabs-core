from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca
    data = getData()
    ca = p.api.action.racktivity

def teardown():
    racktivity_test_library.backplane.delete(backplane1Guid)
    racktivity_test_library.backplane.delete(backplane2Guid)

def testCreate_1():
    """
    @description: [0020201] Creating backplane by calling create function and passing only the non optional parameters
    @id: 0020201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.create('test_backplane1', 'ETHERNET')['result']['backplaneguid']
    @expected_result: function should create backplane and store it in the drp
    """
    global backplane1Guid
    q.logger.log("         Creating Backplane")
    backplane1Guid = ca.backplane.create('test_backplane1', 'ETHERNET')['result']['backplaneguid']
    ok_(backplane1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if backplane exists")
    backplane1 = ca.backplane.getObject(backplane1Guid)
    assert_equal(backplane1.name,'test_backplane1')
    assert_equal(backplane1.backplanetype,q.enumerators.backplanetype.ETHERNET)

def testCreate_2():
    """
    @description: [0020202] Creating backplane by calling create function and passing all parameters (both optional and required parameters)
    @id: 0020202
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.create('test_backplane2', 'INFINIBAND', 'test_backplane2_description', True, True, True)['result']['backplaneguid']
    @expected_result: function should create backplane and store it in the drp
    """
    global backplane2Guid
    q.logger.log("         Creating Backplane with optional params")
    backplane2Guid = ca.backplane.create('test_backplane2', 'INFINIBAND', 'test_backplane2_description', True, True, True)['result']['backplaneguid']
    ok_(backplane2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if backplane exists")
    backplane2 = ca.backplane.getObject(backplane2Guid)
    assert_equal(backplane2.name,'test_backplane2')
    assert_equal(backplane2.backplanetype,q.enumerators.backplanetype.INFINIBAND)
    assert_equal(backplane2.description,'test_backplane2_description')
    assert_equal(backplane2.publicflag, True)
    assert_equal(backplane2.managementflag, True)
    assert_equal(backplane2.storageflag, True)

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0020203] Creating backplane by calling create function and passing a number as name instead of string
    @id: 0020203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.create(7, 'ETHERNET')
    @expected_result: function should fail because integers are not allowed as names
    """
    q.logger.log("         Creating backplane with Integer as name")
    ca.backplane.create(7, 'ETHERNET')

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0020204] Creating backplane by calling create function and passing an invalid backplane type
    @id: 0020204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.create('test_backplane3', 'INVALID')
    @expected_result: function should fail because you must pass a valid backplane type when creating a backplane
    """
    q.logger.log("         Creating backplane with invalid backplane type")
    ca.backplane.create('test_backplane3', 'INVALID')

@raises(xmlrpclib.Fault)
def testCreate_5():
    """
    @description: [0020205] Creating backplane with a name that already exists
    @id: 0020205
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.create('test_backplane1', 'ETHERNET')
    @expected_result: function should fail because backplane name is unique
    """
    q.logger.log("         Creating backplane with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

