from nose.tools import *
from pylabs import i,q
import racktivity_test_library
from . import getData

def setup():
    global ca, lvguid, dcGuids, data
    data = getData()
    ca = data["ca"]
    lvguid = racktivity_test_library.logicalview.create("test_logicalview1")
    dcGuids = [data["dc1"],data["dc2"]]

def teardown():
    ca.logicalview.delete(lvguid)

def TestGetPduHealthStatus_1():
    """
    @description: [0253101] this function will call logicalviews that searches for rootobjects and get statsitics about their pdus 
    @id: 0.25.31.01
    @timestamp: 1297099779
    @signature: mmagdy
    @params: viewstring=""
    @expected_result: function should succeed
    """
    import time
    currenttime = int(time.time())
    
    md1 = q.drp.meteringdevice.get(data["mdguid1"])
    md1.lastaccessed = currenttime
    q.drp.meteringdevice.save(md1)
    md2 = q.drp.meteringdevice.get(data["mdguid2"])
    md2.lastaccessed = currenttime - 100
    q.drp.meteringdevice.save(md2)
    md3 = q.drp.meteringdevice.get(data["mdguid3"])
    md3.lastaccessed = currenttime - 1000
    q.drp.meteringdevice.save(md3)
    
    ca.logicalview.updateModelProperties(lvguid, viewstring="parenttree:{datacenter:DC1}")
    result = ca.logicalview.getPduHealthStatus(lvguid, [60,600])['result']['healthstatus']
    assert_equals(len(result), 3, "Expected 3 iitems got %d instead"%len(result))
    assert_equals(result, [1, 1, 1], "unexpected result %s "%str(result))
