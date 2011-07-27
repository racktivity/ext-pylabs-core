from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, usrGuid1
    ca = p.api.action.racktivity
    usrGuid1 = racktivity_test_library.clouduser.create("test_clouduser1")

def teardown():
    racktivity_test_library.clouduser.delete(usrGuid1)

def testUpdate_1():
    """
    @description: [0051701]Updating clouduser name
    @id: 0051701
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.updateModelProperties(usrGuid1, name = "test_clouduser_rename")
    @expected_result: clouduser name should be updated
    """
    q.logger.log("         Updating clouduser name")
    ca.clouduser.updateModelProperties(usrGuid1, name = "test_clouduser_rename")
    usr = ca.clouduser.getObject(usrGuid1)
    assert_equal(usr.name, "test_clouduser_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0051702]Updating clouduser Description
    @id: 0051702
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.updateModelProperties(usrGuid1, description = "myDescription")
    @expected_result: clouduser description should be updated
    """
    q.logger.log("         Updating clouduser Description")
    ca.clouduser.updateModelProperties(usrGuid1, description = "myDescription")
    usr = ca.clouduser.getObject(usrGuid1)
    assert_equal(usr.description, "myDescription", "Description attribute was not properly updated")

