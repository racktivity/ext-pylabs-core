from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, feedGuid1, dcguid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    feedGuid1 = racktivity_test_library.feed.create("test_feed1", dcguid)

def teardown():
    racktivity_test_library.feed.delete(feedGuid1)

def testUpdate_1():
    """
    @description: [0231701] Updating feed name
    @id: 0231701
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.updateModelProperties(feedGuid1, name = "test_Feed_rename")
    @expected_result: feed name should be updated in the drp
    """
    q.logger.log("         Updating feed name")
    ca.feed.updateModelProperties(feedGuid1, name = "test_Feed_rename")
    feed = ca.feed.getObject(feedGuid1)
    assert_equal(feed.name, "test_Feed_rename", "Name attribute was not properly updated")

def testUpdate_2():
    """
    @description: [0231702] Updating feed description
    @id: 0231702
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.updateModelProperties(feedGuid1, description = "test_Feed_rename")
    @expected_result: feed description should be updated in the drp
    """
    q.logger.log("         Updating feed description")
    ca.feed.updateModelProperties(feedGuid1, description = "test_Feed_rename")
    feed = ca.feed.getObject(feedGuid1)
    assert_equal(feed.description, "test_Feed_rename", "Description attribute was not properly updated")

def testUpdate_3():
    """
    @description: [0231703] Updating feed co2emission
    @id: 0231703
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.updateModelProperties(feedGuid1, co2emission = 930.0)
    @expected_result: feed co2emission should be added to the dictionary
    """
    q.logger.log("         Updating feed co2emission")
    ca.feed.updateModelProperties(feedGuid1, co2emission = 930.0)
    feed = ca.feed.getObject(feedGuid1)
    ok_(930.0 in feed.co2emission.values() , "Feed co2emission was not properly updated")
