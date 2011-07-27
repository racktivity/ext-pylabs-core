from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p
from . import getData

def setup():
    global ca, dcguid, feedGuid, cableGuid
    data = getData()
    ca = p.api.action.racktivity
    dcguid = data["dcguid"]
    feedGuid = racktivity_test_library.feed.create("test_feed1", dcguid)
    ca.feed.addConnector(feedGuid, "MyConn", 0, "BROKEN")
    cableGuid = racktivity_test_library.cable.create()

def teardown():
    ca.feed.delete(feedGuid)
    ca.cable.delete(cableGuid)

def testConnectConnector_1():
    """
    @description: [0232401] Connecting connector to cable
    @id: 0232401
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.connectConnector(feedGuid, "MyConn", cableGuid)['result']['returncode']
    @expected_result: operation should succeed and returncode should be True
    """
    ok_(ca.feed.connectConnector(feedGuid, "MyConn", cableGuid)['result']['returncode'])

@raises(xmlrpclib.Fault)
def testConnectConnector_2():
    """
    @description: [0232402] Connecting non existing connector to cable
    @id: 0232402
    @timestamp: 1293552891
    @signature: mmagdy
    @params: ca.feed.connectConnector(feedGuid, "MyConn2", cableGuid)
    @expected_result: operation should fail because connector's name doesn't exist
    """
    ca.feed.connectConnector(feedGuid, "MyConn2", cableGuid)

