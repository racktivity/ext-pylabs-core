from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, usrGuids, exList
    ca = i.config.cloudApiConnection.find("main")
    exList = ca.clouduser.find("")["result"]["guidlist"]
    usrGuid1 = racktivity_test_library.clouduser.create("test_clouduser1")
    usrGuid2 = racktivity_test_library.clouduser.create("test_clouduser2")
    usrGuids = (usrGuid1,usrGuid2)

def teardown():
    for guid in usrGuids:
        racktivity_test_library.clouduser.delete(guid)

def testList_1():
    """
    @description: [0051101] this function will create some cloudusers and for each created clouduser a list function is called with this clouduser's guid and make sure that the function succeed
    @id: 0051101
    @timestamp: 1293360198
    @signature: mmagdy
    @params:for guid in createdCoudusersGuids: ca.clouduser.list(guid)['result']['cloudusersinfo']
    @expected_result: function should succeed
    """
    q.logger.log("make sure all the Cloudusers I created are listed by list(guid) call")
    for guid in usrGuids:
        result = ca.clouduser.list(guid)['result']['clouduserinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0051102] this function will call the list function without any parameters and validate its output
    @id: 0051102
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.list()
    @expected_result: function should return a list that contains information about the cloudusers I have created
    """
    q.logger.log("make sure that list() only returns the cloudusers I created")
    result = ca.clouduser.list()['result']['clouduserinfo']
    for info in result:
        #We must skip the admin account
        if info['guid'] in exList: continue
        ok_(info['guid'] in usrGuids, "clouduser %s was returned by list() but I didn't create this clouduser"%info['guid'])

