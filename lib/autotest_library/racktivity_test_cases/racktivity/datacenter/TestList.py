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

def testList_1():
    """
    @description: [0081101] his function will create some datacenters and for each created datacenter a list function is called with this datacenter's guid and make sure that the function succeed
    @id: 0081101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in datacenterGuids: ca.datacenter.list(guid)['result']['datacenterinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each datacenter to make sure its listed")
    for guid in dcGuids:
        result = ca.datacenter.list(guid)['result']['datacenterinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0081102] this function will call the list function without any parameters and validate its output
    @id: 0081102
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for info in ca.datacenter.list()['result']['datacenterinfo']: assert(info['guid'] in dcGuids)
    @expected_result: function should return a list that contains information about the datacenter I have created
    """
    q.logger.log("calling list once and make sure it only returns the datacenters I created")
    result = ca.datacenter.list()['result']['datacenterinfo']
    for info in result:
        assert_true(info['guid'] in dcGuids, "datacenter %s was returned by list() but I didn't create this datacenter"%info['guid'])
