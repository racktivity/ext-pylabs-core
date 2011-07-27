from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, backplaneGuids, roomguid, exList
    data = getData()
    ca = p.api.action.racktivity
    exList = ca.backplane.find("")["result"]["guidlist"]
    backplaneGuid1 = racktivity_test_library.backplane.create("test_backplane1")
    backplaneGuid2 = racktivity_test_library.backplane.create("test_backplane2")
    backplaneGuids = (backplaneGuid1,backplaneGuid2) 

def teardown():
    for guid in backplaneGuids:
        racktivity_test_library.backplane.delete(guid)

def testList_1():
    """
    @description: [0021101] this function will create some backplanes and for each created backplane a list function is called with this backplane's guid and make sure that the function succeed
    @id: 0021101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdBackplaneGuids: ca.backplane.list(guid)['result']['backplaneinfo']
    @expected_result: function should succeed
    """
    q.logger.log("make sure all the backplanes I created are listed by list() call")
    for guid in backplaneGuids:
        result = ca.backplane.list(guid)['result']['backplaneinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['backplaneguid'], guid, "list returned guid %s expected %s"%(result[0]['backplaneguid'], guid))

def testList_2():
    """
    @description: [0021102] this function will call the list function without any parameters and validate its output
    @id: 0021102
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.backplane.list()['result']['backplaneinfo']
    @expected_result: function should return a list that contains information about the backplanes I have created
    """
    q.logger.log("make sure that list() only returns the backplanes I created")
    result = ca.backplane.list()['result']['backplaneinfo']
    for info in result:
        if info['backplaneguid'] in exList: continue
        ok_(info['backplaneguid'] in backplaneGuids, "backplane %s was returned by list() but I didn't create this backplane"%info['backplaneguid'])
