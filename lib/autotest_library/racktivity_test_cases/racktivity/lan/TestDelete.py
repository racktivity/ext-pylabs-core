from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, lanGuid
    data = getData()
    ca = p.api.action.racktivity
    lanGuid = racktivity_test_library.lan.create('test_lan1',data['backplaneguid1'])

def teardown():
    pass

def testDelete_1():
    """
    @description: [0140301] Deleting Previously created lan
    @id: 0140301
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.delete(lanGuid)
    @expected_result: function should succeed because guid used is a valid lan guid 
    """
    q.logger.log("    Deleting Previously created lan")
    ca.lan.delete(lanGuid)
    assert_raises(xmlrpclib.Fault, ca.lan.getObject, lanGuid)

@raises(xmlrpclib.Fault)
def testDelete_2():
    """
    @description: [0140302] Deleting non existing lan
    @id: 0140302
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.lan.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail because guid used is not a valid lan guid (no lan with this guid exists)
    """
    q.logger.log("    Deleting non existing lan")
    ca.lan.delete('00000000-0000-0000-0000-000000000000')

