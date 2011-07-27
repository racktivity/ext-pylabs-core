from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, rowGuids
    data = getData()
    ca = p.api.action.racktivity
    pod1Guid = data["pod1"]
    row1Guid = racktivity_test_library.row.create(pod1Guid, 'test_row1')
    row2Guid = racktivity_test_library.row.create(pod1Guid, 'test_row2')
    rowGuids = (row1Guid,row2Guid)

def teardown():
    for guid in rowGuids:
        racktivity_test_library.row.delete(guid)

def testList_1():
    """
    @description: [0.35.11.01] his function will create some rows and for each created row a list function is called with this row's guid and make sure that the function succeed
    @id: 0.35.11.01
    @timestamp: 1298812206
    @signature: halimm
    @params: for guid in rowGuids: ca.row.list(guid)['result']['rowinfo']
    @expected_result: function should succeed
    """
    q.logger.log("calling list for each row to make sure its listed")
    for guid in rowGuids:
        result = ca.row.list(guid)['result']['rowinfo']
        assert_equal(len(result), 1, "Expected a single guid in the result when calling list with guid %s got %d instead"%(guid,len(result)))
        assert_equal(result[0]['guid'], guid, "list returned guid %s expected %s"%(result[0]['guid'], guid))

def testList_2():
    """
    @description: [0.35.11.02] this function will call the list function without any parameters and validate its output
    @id: 0.35.11.02
    @timestamp: 1298812206
    @signature: halimm
    @params: for info in ca.row.list()['result']['rowinfo']: assert(info['guid'] in rowGuids)
    @expected_result: function should return a list that contains information about the row I have created
    """
    q.logger.log("calling list once and make sure it only returns the rows I created")
    result = ca.row.list()['result']['rowinfo']
    for info in result:
        assert_true(info['guid'] in rowGuids, "row %s was returned by list() but I didn't create this row"%info['guid'])
