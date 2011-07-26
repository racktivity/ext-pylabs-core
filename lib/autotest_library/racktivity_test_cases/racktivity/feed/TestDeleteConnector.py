from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, dcguid, feedGuid
    data = getData()
    ca = data["ca"]
    dcguid = data["dcguid"]
    feedGuid = racktivity_test_library.feed.create("test_feed1", dcguid)
    ca.feed.addConnector(feedGuid, "MyConn", 0, "BROKEN")

def teardown():
    ca.feed.delete(feedGuid)

def testDeleteConnector_1():
    """
    @description: [0232401] Deleting connector to feed object
    @id: 0232401
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.deleteConnector(feedGuid, "MyConn", 0, "BROKEN")
    @expected_result: operation should succeed and returncode should be True
    """
    ok_(ca.feed.deleteConnector(feedGuid, "MyConn")['result']['returncode'])

@raises(cloud_api_client.Exceptions.CloudApiException)
def testDeleteConnector_2():
    """
    @description: [0232402] Deleting non existing connector
    @id: 0232402
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.deleteConnector(feedGuid, "MyConn2")
    @expected_result: operation should fail because connector's name doesn't exist
    """
    ca.feed.deleteConnector(feedGuid, "MyConn2")

