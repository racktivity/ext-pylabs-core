from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q

def setup():
    global cloudapi
    cloudapi = i.config.cloudApiConnection.find("main")
    
def teardown():
    pass

def testCreate_1():
    """
    @description: [0.33.02.01] Creating enterprise by calling create function and passing only the non optional parameters
    @id: 0.33.02.01
    @timestamp: 1298552890
    @signature: halimm
    @params: cloudapi.enterprise.create()['result']['enterpriseguid']
    @expected_result: function should create enterprise and store it in the drp
    """
    global guid
    q.logger.log("         Creating enterprise")
    guid = cloudapi.enterprise.create('enterprise')['result']['enterpriseguid']
    q.logger.log("         Checking if enterprise exists")
    ok_(guid, "Empty guid returned from create function")
    racktivity_test_library.enterprise.delete(guid)

def testCreate_2():
    """
    @description: [0.33.02.02] Creating enterprise by calling create function and passing all parameters (both optional and required parameters)
    @id: 0.33.02.02
    @timestamp: 1298552890
    @signature: halimm
    @params:cloudapi.enterprise.create('test_enterprise_optional', 'Test Description', [locGuid1])['result']['enterpriseguid']
    @expected_result: function should create enterprise and store it in the drp
    """
    q.logger.log("         Creating enterprise with optional params")
    guid = cloudapi.enterprise.create('test_enterprise_optional', 'Test Description')['result']['enterpriseguid']
    ok_(guid, "Empty guid returned from create function")
    q.logger.log("         Checking if enterprise exists")
    ent2 = cloudapi.enterprise.getObject(guid)
    ok_(ent2.name == 'test_enterprise_optional', "Name of resource group is different than the name given to it during creation")
    racktivity_test_library.enterprise.delete(guid)

def testCreate_3():
    """
    @description: [0.33.02.03] Creating enterprise by calling create function and passing a number as name instead of string
    @id: 0.33.02.03
    @timestamp: 1298552890
    @signature: halimm
    @params:cloudapi.enterprise.create(name=7)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating enterprise with Integer as name")
    assert_raises(cloud_api_client.Exceptions.CloudApiException, cloudapi.enterprise.create, name= 7)

def testCreate_4():
    """
    @description: [0.33.02.05] Creating multiple enterprise objects
    @id: 0.33.02.05
    @timestamp: 1298552890
    @signature: halimm
    @params:cloudapi.enterprise.create('test_enterprise_optional')['result']['enterpriseguid']
    @expected_result: function should fail because enterprise name must be unique
    """
    q.logger.log("         Creating enterprise with the same name by calling testCreate_Positive() again")
    guid = cloudapi.enterprise.create("enterprise1")['result']['enterpriseguid']
    assert_raises(cloud_api_client.Exceptions.CloudApiException, cloudapi.enterprise.create, "enterprise2")
    racktivity_test_library.enterprise.delete(guid)


