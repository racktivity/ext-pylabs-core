from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, feedGuids, dcguid
    data = getData()
    ca = data["ca"]
    dcguid = data["dcguid"]
    feedGuid1 = racktivity_test_library.feed.create("test_feed1", dcguid)
    feedGuid2 = racktivity_test_library.feed.create("test_feed2", dcguid)
    feedGuids = (feedGuid1,feedGuid2) 

def teardown():
    for guid in feedGuids:
        racktivity_test_library.feed.delete(guid)

def testList_1():
    """
    @description: [0231101] this function will create some feeds and for each created feed a list function is called with this feed's guid and make sure that the function succeed
    @id: 0231101
    @timestamp: 1293552891
    @signature: mmagdy
    @params: for guid in createdFeedGuids: feed.list(guid)['result']['feedinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each feed to make sure its listed")
    for guid in feedGuids:
        result = ca.feed.list(guid)['result']['feedinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0231102] this function will call the list function without any parameters and validate its output
    @id: 0231102
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.list()['result']['feedinfo']
    @expected_result: function should return a list that contains information about the feed I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.feed.list()['result']['feedinfo']
    guids = map(lambda i: i['guid'], result)
    for guid in feedGuids:
        ok_(guid in guids, "Feed '%s' not returned by the list method" % guid)
