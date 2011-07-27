from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p

def setup():
    global ca
    ca = p.api.action.racktivity

def teardown():
    racktivity_test_library.location.delete(loc1Guid)
    racktivity_test_library.location.delete(loc2Guid)

def testCreate_1():
    """
    @description: [0150201] Creating Location by calling create function and passing only the non optional parameters
    @id: 0150201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.create('test_Location1')['result']['locationguid']
    @expected_result: function should create Location and store it in the drp
    """
    global loc1Guid
    q.logger.log("         Creating Location")
    loc1Guid = ca.location.create('test_Location1')['result']['locationguid']
    ok_(loc1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if location exists")
    loc1 = ca.location.getObject(loc1Guid)

def testCreate_2():
    """
    @description: [0150202] Creating Location by calling create function and passing all parameters (both optional and required parameters)
    @id: 0150202
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.create('test_Location2', 'test_Location_description', 'test_Location_alias',
    @expected_result: function should create Location and store it in the drp
                                  'test_Location_address', 'test_Location_city', 'test_Location_country',
                                  public=True)['result']['locationguid']
    """
    global loc2Guid
    q.logger.log("         Creating Location")
    loc2Guid = ca.location.create('test_Location2', 'test_Location_description', 'test_Location_alias',
                                  'test_Location_address', 'test_Location_city', 'test_Location_country',
                                  public=True)['result']['locationguid']
    ok_(loc2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if location exists")
    loc2 = ca.location.getObject(loc2Guid)

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0150203] Creating Location by calling create function and passing a number as name instead of string
    @id: 0150203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.create(7)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating location with Integer as name")
    ca.location.create(7)

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0150204] Creating location with the same name by
    @id: 0150204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.create('test_Location1')['result']['locationguid']
    @expected_result: function should fail because location name must be unique
    """
    q.logger.log("         Creating location with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

