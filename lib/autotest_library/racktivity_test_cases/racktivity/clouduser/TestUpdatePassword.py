from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, usrGuid1
    ca = i.config.cloudApiConnection.find("main")
    usrGuid1 = racktivity_test_library.clouduser.create(password="123")

def teardown():
    racktivity_test_library.clouduser.delete(usrGuid1)

def testUpdatePassword_1():
    """
    @description: [0051801] changing user password
    @id: 0051801
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.updatePassword(usrGuid1, "123", "abc")
    @expected_result: user password should be changed
    """
    q.logger.log("         updating user password")
    ca.clouduser.updatePassword(usrGuid1, "123", "abc")
    usr = ca.clouduser.getObject(usrGuid1)
    assert_equal(usr.password, "abc", "Password update failed")
    #Revert password to its original value
    ca.clouduser.updatePassword(usrGuid1, "abc", "123")


@raises(cloud_api_client.Exceptions.CloudApiException)
def testUpdatePassword_2():
    """
    @description: [0051802] changing user password with invalid 'current password' parameter
    @id: 0051802
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.updatePassword(usrGuid1, "invalidPassword", "mypass")
    @expected_result: updating password should fail because current password is invalid
    """
    q.logger.log("         updating user password with invalid 'current password' parameter" )
    ca.clouduser.updatePassword(usrGuid1, "invalidPassword", "mypass")

