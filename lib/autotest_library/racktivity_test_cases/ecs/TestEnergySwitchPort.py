from pylabs import q
from nose.tools import *
from . import getClient

TEST_IP = "111.222.333.444"
TEST_ES_NAME = "test_es_p_name_123456"
TEST_GR_NAME = "test_gr_p_name_123456"
TEST_PRT_INDEX = 100
TEST_PRT_INDEX_2 = 200
TEST_TYPE = "ES1008-16"

esid = None

def setup():
    global esid
    client = getClient()
    client.energyswitch.add(TEST_IP, TEST_ES_NAME, TEST_TYPE)
    es = client.energyswitch.get(TEST_ES_NAME)
    esid = es['energyswitchid']

def teardown():
    global esid
    client = getClient()
    client.energyswitch.delete(esid)

def testESPRT_1():
    """
    @description: [ECS.4.1] Add port to energyswitch
    @id: ECS.4.1
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitchport.add(esid, index)
    @expected_result: function should add port to energy switch
    """
    client = getClient()
    global esid
    
    client.energyswitchport.add(esid, TEST_PRT_INDEX)
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX)
    assert_true(port, "Port wasn't added successfully")

def testESPRT_2():
    """
    @description: [ECS.4.2] List energyswitch ports
    @id: ECS.4.2
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitchport.list(id)
    @expected_result: function should return a list of all ports assigned to an energyswitch
    """
    client = getClient()
    global esid
    ports = client.energyswitchport.list(esid)
    found = False
    for prt in ports:
        if prt['portindex'] == TEST_PRT_INDEX:
            found = True
            break
    
    assert_true(found, "The port was not found by list")

def testESPRT_3():
    """
    @description: [ECS.4.3] Check if a port exists by its id 
    @id: ECS.4.3
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitchport.exists(portid)
    @expected_result: function should return true if energyswitche port with the given id exists
    """
    client = getClient()
    global esid
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX)
    assert_true(client.energyswitchport.exists(port['portid']), "The port was not found")

def testESPRT_4():
    """
    @description: [ECS.4.4] Port delete 
    @id: ECS.4.4
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitchport.delete(portid)
    @expected_result: function should delete a port
    """
    client = getClient()
    global esid
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX)
    client.energyswitchport.delete(port['portid'])
    
    assert_false(client.energyswitchport.exists(port['portid']), "port wasn't deleted successfully")

def testESPRT_5():
    """
    @description: [ECS.4.5] Do setGroups on port
    @id: ECS.4.5
    @timestamp: 1301304493
    @signature: mazmy
    @params: client.energyswitchport.setGroups(portid, user, restricted)
    @expected_result: function should set groups on port
    """
    client = getClient()
    global esid
    client.energyswitchport.add(esid, TEST_PRT_INDEX_2)
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    usergrp = "port_user_group1"
    restgrp = "port_rest_group1"
    
    client.energyswitchport.setGroups(port['portid'], usergrp, restgrp)
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    
    assert_true(port['user'] == usergrp, "User group wasn't set correctly")
    assert_true(port['restricted'] == restgrp, "Restricted group wasn't set correctly")
    
def testESPRT_6():
    """
    @description: [ECS.4.6] Do setUser on port
    @id: ECS.4.6
    @timestamp: 1301304493
    @signature: mazmy
    @params: client.energyswitchport.setUser(portid, user)
    @expected_result: function should set user group on port
    """
    client = getClient()
    global esid
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    usergrp = "port_user_group111"
    
    client.energyswitchport.setUser(port['portid'], usergrp)
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    
    assert_true(port['user'] == usergrp, "User group wasn't set correctly")
    
def testESPRT_7():
    """
    @description: [ECS.4.7] Do setRestricted on port
    @id: ECS.4.7
    @timestamp: 1301304493
    @signature: mazmy
    @params: client.energyswitchport.setRestricted(portid, user, restricted)
    @expected_result: function should set restricted group on port
    """
    client = getClient()
    global esid
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    restgrp = "port_rest_group1111"
    
    client.energyswitchport.setRestricted(port['portid'], restgrp)
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    assert_true(port['restricted'] == restgrp, "Restricted group wasn't set correctly")

def testESPRT_8():
    """
    @description: [ECS.4.8] Do update on port
    @id: ECS.4.8
    @timestamp: 1301304493
    @signature: rvanover
    @params: client.energyswitchport.update(portid, user, restricted)
    @expected_result: function should set user- and restricted group on port
    """
    client = getClient()
    global esid
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    usergrp = "port_rest_group0000"
    restgrp = "port_rest_group1111"
    
    client.energyswitchport.update(port['portid'], usergrp, restgrp)
    port = client.energyswitchport.get(esid, TEST_PRT_INDEX_2)
    assert_true(port['user'] == usergrp, "User group wasn't set correctly")
    assert_true(port['restricted'] == restgrp, "Restricted group wasn't set correctly")