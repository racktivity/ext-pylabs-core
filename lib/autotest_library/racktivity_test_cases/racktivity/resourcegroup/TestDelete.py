from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, resgGuid
    ca = p.api.action.racktivity
    resgGuid = racktivity_test_library.resourcegroup.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [2450301] Deleting Previously created resourcegroup
    @id: 2450301
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.delete(resgGuid)
    @expected_result: delete operation succeed and this resourcegroup's info/object can no longer be retrieved from the drp
    """
    q.logger.log("    Deleting Previously created resourcegroup")
    ca.resourcegroup.delete(resgGuid)
    assert_raises(xmlrpclib.Fault, ca.resourcegroup.getObject, resgGuid)

def testDelete_2():
    """
    @description: [2450302] Deleting non existing resourcegroup
    @id: 2450302
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.resourcegroup.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: delete operation fails because the guid is invalid
    """
    q.logger.log("    Deleting non existing resourcegroup")
    assert_raises(xmlrpclib.Fault, ca.resourcegroup.delete, '00000000-0000-0000-0000-000000000000')
