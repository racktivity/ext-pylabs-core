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

def teardown():
    ca.feed.delete(feedGuid)

def addConnector_1():
    """
    @description: [0232301] Adding connector to feed object
    @id: 0232301
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.addConnector(feedGuid, "MyConn", 0, "BROKEN")
    @expected_result: operation should succeed and returncode should be True
    """
    ok_(ca.feed.addConnector(feedGuid, "MyConn", 0, "BROKEN")['result']['returncode'])

@raises(cloud_api_client.Exceptions.CloudApiException)
def addConnector_2():
    """
    @description: [0232302] Adding connector with the same name
    @id: 0232302
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.addConnector(feedGuid, "MyConn2", 0, "BROKEN")
    @expected_result: operation should fail because name is unique
    """
    ca.feed.addConnector(feedGuid, "MyConn", 1, "BROKEN")

