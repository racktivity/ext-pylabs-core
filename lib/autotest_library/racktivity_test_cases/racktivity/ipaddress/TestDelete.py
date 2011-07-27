from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, ipGuid
    ca = p.api.action.racktivity
    ipGuid = racktivity_test_library.ipaddress.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [0120301] Deleting Previously created ipaddress
    @id: 0120301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.delete(ipGuid)
    @expected_result:the ipaddress should be deleted
    """
    q.logger.log("    Deleting Previously created ipaddress")
    ca.ipaddress.delete(ipGuid)
    assert_raises(xmlrpclib.Fault, ca.ipaddress.getObject, ipGuid)


@raises(xmlrpclib.Fault)
def testDelete_2():
    """
    @description: [0120302] Deleting non existing ipaddress
    @id: 0120302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.ipaddress.delete('00000000-0000-0000-0000-000000000000')
    @expected_result:the ipaddress should be deleted
    """
    q.logger.log("    Deleting non existing ipaddress")
    ca.ipaddress.delete('00000000-0000-0000-0000-000000000000')

