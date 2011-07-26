from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, dcGuid, locGuid1
    data = getData()
    ca = data["ca"]
    locGuid1 = data["locGuid1"]
    dcGuid = racktivity_test_library.datacenter.create('test_DataCenter1', locGuid1)

def teardown():
    pass

def testDelete_1():
    """
    @description: [0080301] Deleting Previously created datacenter
    @id: 0080301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.delete(dcGuid)
    @expected_result:the datacenter should be deleted
    """
    q.logger.log("    Deleting Previously created datacenter")
    dc1 = ca.datacenter.getObject(dcGuid)
    ca.datacenter.delete(dcGuid)
    assert_raises(cloud_api_client.Exceptions.CloudApiException, ca.datacenter.getObject, dcGuid)
    racktivity_test_library.ui.doUITest("Real+time+data", "DELETE", value=dc1.name)
    ok_(racktivity_test_library.ui.getResult(dc1.name))

@raises(cloud_api_client.Exceptions.CloudApiException)
def testDelete_2():
    """
    @description: [0080302] Deleting non existing datacenter
    @id: 0080302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the datacenter doesn't exist
    """
    q.logger.log("    Deleting non existing datacenter")
    ca.datacenter.delete('00000000-0000-0000-0000-000000000000')

