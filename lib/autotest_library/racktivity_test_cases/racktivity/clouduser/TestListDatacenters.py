from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, usrGuid, dcGuids, locGuid
    ca = p.api.action.racktivity
    usrGuid = racktivity_test_library.clouduser.create()
    locGuid = racktivity_test_library.location.create()
    dcGuids = list()
    for c in xrange(0,3):
       dcGuids.append(racktivity_test_library.datacenter.create("test_datacenter%d"%c,locGuid, clouduserguid=usrGuid))

def teardown():
    racktivity_test_library.location.delete(locGuid)
    racktivity_test_library.clouduser.delete(usrGuid)

def testListDatacenters_1():
    """
    @description: [0051001] Listing datacenters of a clouduser guid
    @id: 0051001
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.listDatacenters(usrGuid)['result']['guidlist']
    @expected_result: function should return datacenters attached to this clouduser
    """
    q.logger.log("        Listing datacenters of a valid clouduser guid")
    result = ca.clouduser.listDatacenters(usrGuid)['result']['guidlist']
    assert_equal(result.sort(), dcGuids.sort(), "the guids returned by listDatacenters() function are not correct")

@raises(xmlrpclib.Fault)
def testListDatacenters_2():
    """
    @description: [0051002]Listing datacenters of an invalid clouduser guid
    @id: 0051002
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.clouduser.listDatacenters('00000000-0000-0000-0000-000000000000')
    @expected_result: function should fail
    """
    q.logger.log("        Listing datacenters of an invalid clouduser guid")
    result = ca.clouduser.listDatacenters('00000000-0000-0000-0000-000000000000')
