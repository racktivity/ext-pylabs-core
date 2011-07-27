from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, locGuid1, usrGuid1
    data = getData()
    ca = p.api.action.racktivity
    locGuid1 = data["locGuid1"]
    usrGuid1 = data["usrGuid1"]

def teardown():
    global dc1Guid, dc2Guid
    racktivity_test_library.datacenter.delete(dc1Guid)
    racktivity_test_library.datacenter.delete(dc2Guid)

def testCreate_1():
    """
    @description: [0080201] Creating Datacenter by calling create function and passing only the non optional parameters
    @id: 0080201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.create('test_DataCenter', locationGuid)['result']['datacenterguid']
    @expected_result: function should create Datacenter and store it in the drp
    """
    global dc1Guid
    q.logger.log("         Creating datacenter")
    dc1Guid = ca.datacenter.create('test_DataCenter', locGuid1)['result']['datacenterguid']
    ok_(dc1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if datacenter exists")
    dc1 = ca.datacenter.getObject(dc1Guid)
    racktivity_test_library.ui.doUITest("Real+time+data", "CREATE", value=dc1.name)
    ok_(racktivity_test_library.ui.getResult( dc1.name))

def testCreate_2():
    """
    @description: [0080202] Creating Datacenter by calling create function and passing all parameters (both optional and required parameters)
    @id: 0080202
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.datacenter.create('test_DataCenter_optional', locationGuid, 'Test Description', usrGuid1 )['result']['datacenterguid']
    @expected_result: function should create Datacenter and store it in the drp
    """
    global dc2Guid
    q.logger.log("         Creating datacenter with optional params")
    dc2Guid = ca.datacenter.create('test_DataCenter_optional', locGuid1, 'Test Description', usrGuid1 )['result']['datacenterguid']
    ok_(dc2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if datacenter exists")
    dc2 = ca.datacenter.getObject(dc2Guid)
    racktivity_test_library.ui.doUITest("Real+time+data", "CREATE", value=dc2.name)
    ok_(racktivity_test_library.ui.getResult(dc2.name))

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0080203] Creating Datacenter by calling create function and passing a number as name instead of string
    @id: 0080203
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.datacenter.create(7, locationGuid)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating datacenter with Integer as name")
    ca.datacenter.create(7, locGuid1)

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0080204] Creating datacenter with Non existing locationguid
    @id: 0080204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.create('test_DataCenter_err' , '00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because locationguid is invalid/doesn't exists
    """
    q.logger.log("         Creating datacenter with Non existing locationguid")
    ca.datacenter.create('test_DataCenter_err' , '00000000-0000-0000-0000-000000000000')

@raises(xmlrpclib.Fault)
def testCreate_5():
    """
    @description: [0080205] Creating datacenter with Non existing clouduserguid
    @id: 0080205
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.create('test_DataCenter_err2' , locGuid1, datacenterguid = '00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because clouduser guid is invalid/doesn't exists 
    """
    q.logger.log("         Creating datacenter with Non existing datacenterguid")
    ca.datacenter.create('test_DataCenter_err2' , locGuid1, clouduserguid = '00000000-0000-0000-0000-000000000000')

@raises(xmlrpclib.Fault)
def testCreate_6():
    """
    @description: [0080206] Creating datacenter with a name that already exists
    @id: 0080206
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.datacenter.create('test_DataCenter', locGuid1)['result']['datacenterguid']
    @expected_result: function should fail because datacenter name must be unique
    """
    q.logger.log("         Creating datacenter with the same name by calling testCreate_Positive() again")
    testCreate_1()

