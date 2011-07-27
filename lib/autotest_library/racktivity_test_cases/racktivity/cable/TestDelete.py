from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, cableGuid
    data = getData()
    ca = p.api.action.racktivity
    cableGuid = racktivity_test_library.cable.create()

def teardown():
    pass

def testDelete_1():
    """
    @description: [0030301]Deleting Previously created cable
    @id: 0030301
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.delete(cableGuid)
    @expected_result: the cable should be deleted
    """
    q.logger.log("    Deleting Previously created cable")
    ca.cable.delete(cableGuid)
    assert_raises(xmlrpclib.Fault, ca.cable.getObject, cableGuid)

@raises(xmlrpclib.Fault)
def testDelete_2():
    """
    @description: [0030302]Deleting non existing cable
    @id: 0030302
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.delete('00000000-0000-0000-0000-000000000000')
    @expected_result: call should fail because the cable doesn't exist
    """
    q.logger.log("    Deleting non existing cable")
    ca.cable.delete('00000000-0000-0000-0000-000000000000')

