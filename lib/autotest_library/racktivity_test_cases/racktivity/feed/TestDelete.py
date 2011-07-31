from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, feedGuid,dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    feedGuid = racktivity_test_library.feed.create("test_feed1", dcguid)

def teardown():
    pass

def testDelete_1():
    """
    @description: [0230301] Deleting Previously created feed
    @id: 0230301
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.delete(feedGuid)
    @expected_result: the feed should be deleted
    """
    q.logger.log("    Deleting Previously created feed")
    feed1 = ca.feed.getObject(feedGuid)
    ca.feed.delete(feedGuid)
    assert_raises(xmlrpclib.Fault, ca.feed.getObject, feedGuid)

def testDelete_2():
    """
    @description: [0230302] Deleting non existing feed
    @id: 0230302
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.delete('00000000-0000-0000-0000-000000000000')
    @expected_result:the feed should be deleted
    """
    q.logger.log("    Deleting non existing feed")
    ok_(ca.feed.delete('00000000-0000-0000-0000-000000000000'), "Deleting a non existing feed returns True")

