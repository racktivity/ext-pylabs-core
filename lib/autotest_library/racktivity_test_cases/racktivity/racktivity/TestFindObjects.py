from nose.tools import *
from pylabs import q, i
import racktivity_test_library

def setup():
    global data
    data = dict()
    data["ca"] = i.config.cloudApiConnection.find("main")
    data["loc"] = racktivity_test_library.location.create("MainLoc", tags="Cairo Egypt company:Info")
    data["dc1"] = racktivity_test_library.datacenter.create("DC1", data["loc"], tags="first datacenter location:Giza")
    data["dc2"] = racktivity_test_library.datacenter.create("DC2", data["loc"], tags="second datacenter location:Cairo")

def teardown():
    ca = p.api.action.racktivity
    ca.location.delete(data["loc"])

def testFindObjects_1():
    """
    @description: [0.40.02.01] Use findObjects to search by tags/labels 
    @id: 0.40.02.01
    @timestamp: 1293361198
    @signature: mina_magdy
    @params: ca.racktivity.findObjects("name: {DC*}, tags_labels: {first && datacenter}")
    @expected_result: should return the first datacenter.
    """
    
    ca = p.api.action.racktivity
    result = ca.racktivity.findObjects("name: {DC*}, tags_labels: {first && datacenter}")["result"]
    assert_equals(len(result), 1)
    result = result[0]
    assert_equals(result["name"] , "DC1")
    assert_equals(result["type"] , "datacenter")

def testFindObjects_2():
    """
    @description: [0.40.02.02] Test findObjects's maxresults and index
    @id: 0.40.02.02
    @timestamp: 1293361198
    @signature: mina_magdy
    @params: ca.racktivity.findObjects("name: {DC*}, tags_labels: {second && datacenter}")
    @expected_result: Should return the second datacenter (DC2).
    """
    
    ca = p.api.action.racktivity
    result = ca.racktivity.findObjects("types:{datacenter}, tags_labels: {datacenter}", maxresults=1, index=1)["result"]
    assert_equals(len(result), 1)
    result = result[0]
    assert_equals(result["name"] , "DC2")
    assert_equals(result["type"] , "datacenter")
