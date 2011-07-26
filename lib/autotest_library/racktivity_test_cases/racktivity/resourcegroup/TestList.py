from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, resgGuids
    ca = i.config.cloudApiConnection.find("main")
    resgGuid1 = racktivity_test_library.resourcegroup.create("test_resourcegroup1")
    resgGuid2 = racktivity_test_library.resourcegroup.create("test_resourcegroup2")
    resgGuids = [resgGuid1,resgGuid2] 

def teardown():
    for guid in resgGuids:
        racktivity_test_library.resourcegroup.delete(guid)

def testList_1():
    """
    @description: [2451101] this function will create some resourcegroups and for each created resourcegroup a list function is called with this resourcegroup's guid and make sure that the function succeed
    @id: 2451101
    @timestamp: 1297089779
    @signature: mmagdy
    @params: for guid in createdLocationGuids: result = ca.resourcegroup.list(guid)['result']['resourcegroupinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each resourcegroup to make sure its listed")
    for guid in resgGuids:
        result = ca.resourcegroup.list(guid)['result']['resourcegroupinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [2451102] this function will call the list function without any parameters and validate its output
    @id: 2451102
    @timestamp: 1297089779
    @signature: mmagdy
    @params: for info in ca.resourcegroup.list()['result']['resourcegroupinfo']: assert(info['guid'] in createdresourcegroupGuids)
    @expected_result: function should return a list that contains information about the resourcegroup I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.resourcegroup.list()['result']['resourcegroupinfo']
    guids = map(lambda i: i['guid'], result)
    for guid in resgGuids:
        ok_(guid in guids, "Can't find resourcegroup '%s' in returned list()" % guid)
        
