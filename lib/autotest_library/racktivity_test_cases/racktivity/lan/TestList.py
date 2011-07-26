from nose.tools import *
import cloud_api_client.Exceptions
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, lanGuids, roomguid
    data = getData()
    ca = data["ca"]
    lanGuid1 = racktivity_test_library.lan.create("test_lan1", data["backplaneguid1"])
    lanGuid2 = racktivity_test_library.lan.create("test_lan2", data["backplaneguid1"])
    lanGuids = (lanGuid1,lanGuid2) 

def teardown():
    for guid in lanGuids:
        racktivity_test_library.lan.delete(guid)

def testList_1():
    """
    @description: [0141101] this function will create some lans and for each created lan a list function is called with this lan's guid and make sure that the function succeed
    @id: 0141101
    @timestamp: 1293360198
    @signature: mmagdy
    @params: for guid in createdLanGuids: ca.lan.list(languid=guid)['result']['laninfo']
    @expected_result: all list calls should succeed and return lan info corresponding to the guid specified
    """
    q.logger.log("calling list for each lan to make sure its listed")
    for guid in lanGuids:
        result = ca.lan.list(languid=guid)['result']['laninfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0141102] this function will call the list function without any parameters and validate its output
    @id: 0141102
    @timestamp: 1293360198
    @signature: mmagdy
    @params:for info in ca.lan.list()['result']['laninfo']: assert(info['guid'] in createdLanGuids)
    @expected_result: function should return list of guids of all the lans I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.lan.list()['result']['laninfo']
    guids = map(lambda i: i['guid'], result)
    for guid in lanGuids:
        ok_(guid in guids, "Can't find lan with guid '%s'" % guid)
