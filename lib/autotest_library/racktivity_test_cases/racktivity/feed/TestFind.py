from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, dcguid, feedGuids
    data = getData()
    ca = data["ca"]
    dcguid = data["dcguid"]
    feed1Guid = racktivity_test_library.feed.create('test_Feed1', dcguid)
    feed2Guid = racktivity_test_library.feed.create('test_Feed2', dcguid)
    feedGuids = (feed1Guid,feed2Guid)

def teardown():
    for guid in feedGuids:
        racktivity_test_library.feed.delete(guid)

def testFind_1():
    """
    @description: [0230401] searching for feed by its name Using find function
    @id: 0230401
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.find(name="test_Feed")['result']['guidlist']
    @expected_result:function should return a valid feed guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.feed.find(name="test_Feed")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in feedGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

