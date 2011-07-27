from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca
    ca = p.api.action.racktivity

def teardown():
    racktivity_test_library.clouduser.delete(usr1Guid)
    racktivity_test_library.clouduser.delete(usr2Guid)

def testCreate_1():
    """
    @description: [0050201]Creating Clouduser by calling create function and passing only the non optional parameters
    @id: 0050201
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.create('test_user1',"pass")['result']['clouduserguid']
    @expected_result: function should create Clouduser and store it in the drp
    """
    global usr1Guid
    q.logger.log("         Creating Clouduser with minimal parameters")
    usr1Guid = ca.clouduser.create('test_user1',"pass")['result']['clouduserguid']
    ok_(usr1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if clouduser exists")
    usr1 = ca.clouduser.getObject(usr1Guid)

def testCreate_2():
    """
    @description: [0050202]Creating Clouduser by calling create function and passing all parameters (both optional and required parameters)
    @id: 0050202
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.create('test_user2', 'pass', 'abc@author.com','test', 'user', 'test user', 'user desc')['result']['clouduserguid']
    @expected_result: function should create Clouduser and store it in the drp
    """
    global usr2Guid
    q.logger.log("         Creating clouduser with full parameters")
    usr2Guid = ca.clouduser.create('test_user2', 'pass', 'abc@author.com',
                                  'test', 'user', 'test user', 'user desc')['result']['clouduserguid']
    ok_(usr2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if clouduser exists")
    usr2 = ca.clouduser.getObject(usr2Guid)

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0050203] Creating Clouduser by calling create function and passing a number as name instead of string
    @id: 0050203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.clouduser.create(7, "pass")
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating clouduser with Integer as name")
    ca.clouduser.create(7, "pass")

@raises(xmlrpclib.Fault)
def testCreate_4():
    """
    @description: [0050204] Creating clouduser with a name that already exists
    @id: 0050204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.clouduser.create('test_user1',"pass")['result']['clouduserguid']
    @expected_result: function should fail because clouduser name is unique
    """
    q.logger.log("         Creating clouduser with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

