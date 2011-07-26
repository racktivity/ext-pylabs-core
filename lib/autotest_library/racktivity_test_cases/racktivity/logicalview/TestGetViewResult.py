from nose.tools import *
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, lvguid, dcGuids
    data = getData()
    ca = data["ca"]
    lvguid = racktivity_test_library.logicalview.create("test_logicalview1")
    dcGuids = [data["dc1"],data["dc2"]]

def teardown():
    ca.logicalview.delete(lvguid)

def TestGetviewresult_1():
    """
    @description: [0251101] this function will call logicalviews that searches for rootobjects with a specific labels and names 
    @id: 0.25.11.01
    @timestamp: 1297089779
    @signature: mmagdy
    @params: viewstring="name: {DC*}, tags_labels: {second && datacenter}"
    @expected_result: function should succeed
    """
    ca.logicalview.updateModelProperties(lvguid, viewstring="name: {DC*}, tags_labels: {second && datacenter}")
    result = ca.logicalview.getViewResult(lvguid)['result']['info']
    assert_equals(len(result), 1, "Expected only one item to be returned in the result got %d instead"%len(result))
    assert_equals(result[0]['guid'], dcGuids[1], "Searching by labels didn't return the expected guid")

def TestGetviewresult_2():
    """
    @description: [0251102] this function will call logicalviews that searches for rootobjects with a specific tags 
    @id: 0.25.11.02
    @timestamp: 1297089779
    @signature: mmagdy
    @params: viewstring="tags_labels: {location:Giza}"
    @expected_result: function should succeed
    """
    ca.logicalview.updateModelProperties(lvguid, viewstring="tags_labels: {location:Giza}")
    result = ca.logicalview.getViewResult(lvguid)['result']['info']
    assert_equals(len(result), 1, "Expected only one item to be returned in the result got %d instead"%len(result))
    assert_equals(result[0]['guid'], dcGuids[0], "Searching by tags didn't return the expected guid")

def TestGetviewresult_3():
    """
    @description: [0251103] this function will call logicalviews that searches for rootobjects with a specific tags and labels
    @id: 0.25.11.03
    @timestamp: 1297089779
    @signature: mmagdy
    @params: viewstring="tags_labels: {location:Giza}"
    @expected_result: function should succeed
    """
    ca.logicalview.updateModelProperties(lvguid, viewstring="tags_labels: {location:Giza && datacenter && first}")
    result = ca.logicalview.getViewResult(lvguid)['result']['info']
    assert_equals(len(result), 1, "Expected only one item to be returned in the result got %d instead"%len(result))
    assert_equals(result[0]['guid'], dcGuids[0], "Searching by tags and labels didn't return the expected guid")
    
#    guids = list()
#    for info in ca.logicalview.getViewResult(lvguid)['result']['info']:
#        guids.append(info[0]['guid'])
#    assert_equals(guids.sort(), dcGuids.sort(), "Searching by labels returned invalid result")
