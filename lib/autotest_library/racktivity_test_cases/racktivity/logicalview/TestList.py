from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library

def setup():
    global ca, lvGuids
    ca = p.api.action.racktivity
    lvGuid1 = racktivity_test_library.logicalview.create("test_logicalview1")
    lvGuid2 = racktivity_test_library.logicalview.create("test_logicalview2")
    lvGuids = [lvGuid1,lvGuid2] 

def teardown():
    for guid in lvGuids:
        racktivity_test_library.logicalview.delete(guid)

def testList_1():
    """
    @description: [0251101] this function will create some logicalviews and for each created logicalview a list function is called with this logicalview's guid and make sure that the function succeed
    @id: 0.25.11.01
    @timestamp: 1297089779
    @signature: mmagdy
    @params: for guid in createdLocationGuids: result = ca.logicalview.list(guid)['result']['logicalviewinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each logicalview to make sure its listed")
    for guid in lvGuids:
        lv = ca.logicalview.getObject(guid)
        result = ca.logicalview.list(lv.name)['result']['logicalviewinfo']
        assert_equal(len(result), 1, "Expected a single logicalview in the result when calling list with name %s got %d instead"%(lv.name,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0251102] this function will call the list function without any parameters and validate its output
    @id: 0.25.11.02
    @timestamp: 1297089779
    @signature: mmagdy
    @params: for info in ca.logicalview.list()['result']['logicalviewinfo']: assert(info['guid'] in createdlogicalviewGuids)
    @expected_result: function should return a list that contains information about the logicalview I have created
    """
    q.logger.log("calling list once and validate the result")
    result = ca.logicalview.list()['result']['logicalviewinfo']
    guids = map(lambda i: i['guid'], result)
    for guid in lvGuids:
        ok_(guid in guids, "Can't find logical view '%s' in the guids returned by list()" % guid)
