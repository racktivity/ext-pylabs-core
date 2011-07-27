from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p

def setup():
    global ca
    ca = p.api.action.racktivity

def teardown():
    racktivity_test_library.logicalview.delete(lv1Guid)

def testCreate_1():
    """
    @description: [0252001] Creating Logicalview by calling create function and passing only the non optional parameters
    @id: 0.25.20.01
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.create('test_Logicalview1')['result']['logicalviewguid']
    @expected_result: function should create Logicalview and store it in the drp
    """
    global lv1Guid
    q.logger.log("         Creating Logicalview")
    lv1Guid = ca.logicalview.create('test_Logicalview1',"types:{energyswitch,datacenter}, tags_labels:{DCLOC && usage:storage}")['result']['logicalviewguid']
    ok_(lv1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if logicalview exists")
    lv1 = ca.logicalview.getObject(lv1Guid)
    ok_(lv1.name == 'test_Logicalview1', "Name of resource group is different than the name given to it during creation")
    ok_(lv1.viewstring == "types:{energyswitch,datacenter}, tags_labels:{DCLOC && usage:storage}", "ViewString of resource group is different than the ViewString given to it during creation")

@raises(xmlrpclib.Fault)
def testCreate_2():
    """
    @description: [0252002] Creating Logicalview by calling create function and passing a number as name instead of string
    @id: 0.25.20.02
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.create(7)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating logicalview with Integer as name")
    ca.logicalview.create(7, "")

@raises(xmlrpclib.Fault)
def testCreate_3():
    """
    @description: [0252003] Creating logicalview with the same name by
    @id: 0.25.20.03
    @timestamp: 1297089779
    @signature: mmagdy
    @params: ca.logicalview.create('test_Logicalview1')['result']['logicalviewguid']
    @expected_result: function should fail because logicalview name must be unique
    """
    q.logger.log("         Creating logicalview with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

