from nose.tools import *
import cloud_api_client.Exceptions
import racktivity_test_library
from pylabs import i,q
from . import getData

def setup():
    global ca
    data = getData()
    ca = data["ca"]

def teardown():
    racktivity_test_library.cable.delete(cable1Guid)
    racktivity_test_library.cable.delete(cable2Guid)

def testCreate_1():
    """
    @description: [0030201] Creating Cable by calling create function and passing only the non optional parameters
    @id: 0030201
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.cable.create('test_cable1', 'USBCABLE')['result']['cableguid']
    @expected_result: function should create Cable and store it in the drp
    """
    global cable1Guid
    q.logger.log("         Creating Cable")
    cable1Guid = ca.cable.create('test_cable1', 'USBCABLE')['result']['cableguid']
    ok_(cable1Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if cable exists")
    cable1 = ca.cable.getObject(cable1Guid)
    assert_equal(cable1.name,'test_cable1')
    assert_equal(cable1.cabletype,q.enumerators.cabletype.USBCABLE)

def testCreate_2():
    """
    @description: [0030202] Creating Cable by calling create function and passing all parameters (both optional and required parameters)
    @id: 0030202
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.create('test_cable2', 'USBCABLE', 'test_cable2_description', 'test_cable2_label')['result']['cableguid']
    @expected_result: function should create Cable and store it in the drp
    """
    global cable2Guid
    q.logger.log("         Creating Cable with optional params")
    cable2Guid = ca.cable.create('test_cable2', 'USBCABLE', 'test_cable2_description', 'test_cable2_label')['result']['cableguid']
    ok_(cable2Guid, "Empty guid returned from create function")
    q.logger.log("         Checking if cable exists")
    cable2 = ca.cable.getObject(cable2Guid)
    assert_equal(cable2.name,'test_cable2')
    assert_equal(cable2.cabletype,q.enumerators.cabletype.USBCABLE)
    assert_equal(cable2.description,'test_cable2_description')
    assert_equal(cable2.label,'test_cable2_label')

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_3():
    """
    @description: [0030203] Creating Cable by calling create function and passing a number as name instead of string
    @id: 0030203
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.create(7, 'USBCABLE')
    @expected_result: function should fail because integers are not allowed as name
    """
    q.logger.log("         Creating cable with Integer as name")
    ca.cable.create(7, 'USBCABLE')

@raises(cloud_api_client.Exceptions.CloudApiException)
def testCreate_4():
    """
    @description: [0030204] Creating cable with a name that already exists
    @id: 0030204
    @timestamp: 1293360198
    @signature: mmagdy
    @params:ca.cable.create('test_cable1', 'USBCABLE')['result']['cableguid']
    @expected_result: function should fail because cable name is unique
    """
    q.logger.log("         Creating cable with the same name by (re)calling testCreate_Positive() again")
    testCreate_1()

