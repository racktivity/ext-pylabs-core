from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, lvGuid
    ca = p.api.action.racktivity
    lvGuid = racktivity_test_library.logicalview.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [2550301] Deleting Previously created logicalview
    @id: 2550301
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.delete(lvGuid)
    @expected_result: delete operation succeed and this logicalview's info/object can no longer be retrieved from the drp
    """
    q.logger.log("    Deleting Previously created logicalview")
    ca.logicalview.delete(lvGuid)
    assert_raises(xmlrpclib.Fault, ca.logicalview.getObject, lvGuid)

def testDelete_2():
    """
    @description: [2550302] Deleting non existing logicalview
    @id: 2550302
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: delete operation fails because the guid is invalid
    """
    q.logger.log("    Deleting non existing logicalview")
    assert_raises(xmlrpclib.Fault, ca.logicalview.delete, '00000000-0000-0000-0000-000000000000')
