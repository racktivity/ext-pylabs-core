from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library

def setup():
    global ca, ipGuid1, ipGuids
    ca = i.config.cloudApiConnection.find("main")
    ip1Guid = racktivity_test_library.ipaddress.create('test_Ipaddress1')
    ip2Guid = racktivity_test_library.ipaddress.create('test_Ipaddress2')
    ipGuids = (ip1Guid,ip2Guid)

def teardown():
    for guid in ipGuids:
        racktivity_test_library.ipaddress.delete(guid)

def testFind_1():
    """
    @description: [0120401] searching for ipaddress by its name Using find function
    @id: 0120401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.find(name="test_Ipaddress")['result']['guidlist']
    @expected_result: function should return a valid ipaddress guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.ipaddress.find(name="test_Ipaddress")['result']['guidlist']
    for guid in ipGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

