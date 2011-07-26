from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca, roomguid
    data = getData()
    ca = data["ca"]
    roomguid = data["roomguid"]

def teardown():
    racktivity_test_library.rack.delete(rack1Guid)
    racktivity_test_library.rack.delete(rack2Guid)

def testCreate_1():
    """
    @description: [0190201] Creating Rack by calling create function and passing only the non optional parameters
    @id: 0190201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.create('test_rack1','OPEN', roomguid)['result']['rackguid']
    @expected_result: function should create Rack and store it in the drp
    """
    global rack1Guid
    q.logger.log("         Creating Rack")
    rack1Guid = ca.rack.create('test_rack1','OPEN', roomguid)['result']['rackguid']
    ok_(rack1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if rack exists")
    rack1 = ca.rack.getObject(rack1Guid)
    assert_equal(rack1.name,'test_rack1')
    assert_equal(rack1.racktype,q.enumerators.racktype.OPEN)
    assert_equal(rack1.roomguid,roomguid)
    racktivity_test_library.ui.doUITest(rack1.roomguid, "CREATE", value=rack1.name)
    ok_(racktivity_test_library.ui.getResult(rack1.name))

def testCreate_2():
    """
    @description: [0190202] Creating Rack by calling create function and passing all parameters (both optional and required parameters)
    @id: 0190202
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.rack.create('test_rack2', 'OPEN', roomguid, 'test_rack2_description', "test_rack2_floor", "test_rack2_corridor","test_rack2_position", 13)['result']['rackguid']
    @expected_result: function should create Rack and store it in the drp
    """
    global rack2Guid
    q.logger.log("         Creating Rack with optional params")
    rack2Guid = ca.rack.create('test_rack2', 'OPEN', roomguid, 'test_rack2_description', "test_rack2_floor", "test_rack2_corridor",
                              "test_rack2_position", 13)['result']['rackguid']
    ok_(rack2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if rack exists")
    rack2 = ca.rack.getObject(rack2Guid)
    assert_equal(rack2.name,'test_rack2')
    assert_equal(rack2.racktype,q.enumerators.racktype.OPEN)
    assert_equal(rack2.roomguid,roomguid)
    assert_equal(rack2.description,'test_rack2_description')
    assert_equal(rack2.floor,'test_rack2_floor')
    assert_equal(rack2.corridor,'test_rack2_corridor')
    assert_equal(rack2.position,'test_rack2_position')
    assert_equal(rack2.height,13)
    racktivity_test_library.ui.doUITest(rack2.roomguid, "CREATE", value=rack2.name)
    ok_(racktivity_test_library.ui.getResult(rack2.name))

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_3():
    """
    @description: [0190203] Creating Rack by calling create function and passing a number as name instead of string
    @id: 0190203
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.create(7, 'OPEN', roomguid)
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating rack with Integer as name")
    ca.rack.create(7, 'OPEN', roomguid)

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_4():
    """
    @description: [0190205] Creating rack with a name that already exists
    @id: 0190204
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.rack.create('test_rack1','OPEN', roomguid)['result']['rackguid']
    @expected_result: function should fail because rack name must be unique
    """
    q.logger.log("         Creating rack with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

