from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q

def setup():
    global ca
    ca = i.config.cloudApiConnection.find("main")

def teardown():
    racktivity_test_library.resourcegroup.delete(resg1Guid)

def testCreate_1():
    """
    @description: [240201] Creating Resourcegroup by calling create function and passing only the non optional parameters
    @id: 240201
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.create('test_Resourcegroup1')['result']['resourcegroupguid']
    @expected_result: function should create Resourcegroup and store it in the drp
    """
    global resg1Guid
    q.logger.log("         Creating Resourcegroup")
    resg1Guid = ca.resourcegroup.create('test_Resourcegroup1', 'Resourcegroup1_desc')['result']['resourcegroupguid']
    ok_(resg1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if resourcegroup exists")
    resg1 = ca.resourcegroup.getObject(resg1Guid)
    ok_(resg1.name == 'test_Resourcegroup1', "Name of resource group is different than the name given to it during creation")
    ok_(resg1.description == 'Resourcegroup1_desc', "Description of resource group is different than the description given to it during creation")

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_2():
    """
    @description: [240202] Creating Resourcegroup by calling create function and passing a number as name instead of string
    @id: 240202
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.create(7)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating resourcegroup with Integer as name")
    ca.resourcegroup.create(7)

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_3():
    """
    @description: [240203] Creating resourcegroup with the same name by
    @id: 240203
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.create('test_Resourcegroup1')['result']['resourcegroupguid']
    @expected_result: function should fail because resourcegroup name must be unique
    """
    q.logger.log("         Creating resourcegroup with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

