from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, dcGuids
    data = getData()
    ca = p.api.action.racktivity
    locGuid1 = data["locGuid1"]
    dc1Guid = racktivity_test_library.datacenter.create('test_DataCenter1', locGuid1)
    dc2Guid = racktivity_test_library.datacenter.create('test_DataCenter2', locGuid1)
    dcGuids = (dc1Guid,dc2Guid) 

def teardown():
    for guid in dcGuids:
        racktivity_test_library.datacenter.delete(guid)

def testFind_1():
    """
    @description: [0080401] searching for datacenter by its name Using find function
    @id: 0080401
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.find(name="test_DataCenter")['result']['guidlist']
    @expected_result: function should return a valid datacenter guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.datacenter.find(name="test_DataCenter*")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in dcGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

