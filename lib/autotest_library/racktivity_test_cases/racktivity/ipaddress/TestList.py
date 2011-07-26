from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, ipGuids
    ca = i.config.cloudApiConnection.find("main")
    ipGuid1 = racktivity_test_library.ipaddress.create("test_ipaddress1")
    ipGuid2 = racktivity_test_library.ipaddress.create("test_ipaddress2")
    ipGuids = (ipGuid1,ipGuid2) 

def teardown():
    for guid in ipGuids:
        racktivity_test_library.ipaddress.delete(guid)

def testList_1():
    """
    @description: [0121101] this function will create some ipaddresss and for each created ipaddress a list function is called with this ipaddress's guid and make sure that the function succeed
    @id: 0121101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdIpGuids: ca.ipaddress.list(guid)['result']['ipaddressinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each ipaddress to make sure its listed")
    for guid in ipGuids:
        result = ca.ipaddress.list(guid)['result']['ipaddressinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0121102] this function will call the list function without any parameters and validate its output
    @id: 0121102
    @timestamp: 1293360198
    @signature: mmagdy
    @params:    for info in result: assert(info['guid'] in ipGuids)
    @expected_result: function should return a list that contains information about the ipaddress I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.ipaddress.list()['result']['ipaddressinfo']
    guids = map(lambda i: i['guid'], result)
    for guid in ipGuids:
        ok_(guid in guids, "Can't find ipaddress '%s' in the ipaddresses returned by list()" % guid)
