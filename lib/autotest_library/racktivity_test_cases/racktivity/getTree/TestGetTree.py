from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, rackGuid1, rackGuid2, row1Guid, data
    data = getData()
    ca = data["ca"]

def testGetTree_1():
    """
    @description: getting direct children of object with one child 
    """
    dc = ca.datacenter.getObject(data["dc1"])
    result = ca.datacenter.getTree(data["dc1"], depth=1)["result"]
    ok_(result["returncode"])
    ok_("tree" in result)
    tree = result["tree"]
    assert_equals(dc.name, tree["name"])
    assert_equals(dc.guid, tree["guid"])
    assert_equals("datacenter", tree["type"])
    assert_equals(len(tree["children"]), 1)
    assert_equals(data['floorguid'], tree["children"][0]["guid"])
    assert_equals("test_floor1", tree["children"][0]["name"])
    assert_equals("floor", tree["children"][0]["type"])


def testGetTree_2():
    """
    @description: getting direct children of object with more than one child
    """
    row = ca.row.getObject(data["rowguid1"])
    result = ca.row.getTree(data["rowguid1"], depth=1)["result"]
    ok_(result["returncode"])
    ok_("tree" in result)
    tree = result["tree"]
    assert_equals(row.name, tree["name"])
    assert_equals(row.guid, tree["guid"])
    assert_equals("row", tree["type"])
    assert_equals(len(tree["children"]), 2)
    rackguids = (data["rackguid1"], data["rackguid2"])
    for idx in range(0,2):
        ok_(tree["children"][idx]["guid"] in rackguids)
        ok_(tree["children"][idx]["name"].startswith("test_rack"), "Returned rack name(s) was invalid (%s)"% tree["children"][idx]["name"])
        assert_equals("rack", tree["children"][idx]["type"])


def testGetTree_3():
    """
    @description: getting full tree, verify the order
    """
    tree = ca.datacenter.getTree(data["dc1"], depth=0)["result"]["tree"]
    order = list()
    while (True):
        order.append(tree["type"])
        if not tree["children"]:
            break
        tree = tree["children"][0]
    assert_equals(order, ['datacenter', 'floor', 'room', 'pod', 'row', 'rack'])
