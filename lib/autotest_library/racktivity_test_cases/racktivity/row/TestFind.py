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

def testFind_1():
    """
    @description: [0.35.04.01] searching for row by its name Using find function
    @id: 0.35.04.01
    @timestamp: 1298812206
    @signature: halimm
    @params: ca.row.find(name="test_row")['result']['guidlist']
    @expected_result: function should return a valid row guid 
    """
    q.logger.log("        Using find function to search by name")
    result = ca.row.find(name="test_row")['result']['guidlist']
    assert_equal(len(result), 2, "Find was expected to return two items %d item(s) were returned instead"%len(result))
    for guid in rowGuids:
        ok_(guid in result, "Guid %s was not returned by find()"%guid)

