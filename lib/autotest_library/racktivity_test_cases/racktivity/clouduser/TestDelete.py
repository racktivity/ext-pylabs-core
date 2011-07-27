from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, usrGuid
    ca = p.api.action.racktivity
    usrGuid = racktivity_test_library.clouduser.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [0050301] Deleting Previously created clouduser
    @id: 0050301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.clouduser.delete(usrGuid)
    @expected_result: the clouduser should be deleted
    """
    q.logger.log("    Deleting Previously created clouduser")
    ca.clouduser.delete(usrGuid)
    assert_raises(xmlrpclib.Fault, ca.clouduser.getObject, usrGuid)

@raises(xmlrpclib.Fault)
def testDelete_2():
    """
    @description: [0050302] Deleting non existing clouduser
    @id: 0050302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.location.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the clouduser doesn't exist
    """
    q.logger.log("    Deleting non existing clouduser")
    ca.clouduser.delete('00000000-0000-0000-0000-000000000000')

