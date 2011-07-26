from pylabs import q
from nose.tools import *
from . import getClient

TEST_IP = "1.2.3.4"
TEST_NAME = "test_name_1234"
TEST_TYPE = "ES1008-16"
TEST_USER = "cn=testUser"
TEST_RESTRICTED = "cn=testRestricted"
TEST_ADMIN = "cn=testAdmin"

def testES_1():
    """
    @description: [ECS.1.1] Add an energy switch
    @id: ECS.1.1
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitch.add(ip, name)
    @expected_result: function should add energy switch to ecs
    """
    client = getClient()
    client.energyswitch.add(TEST_IP, TEST_NAME, TEST_TYPE)
    es = client.energyswitch.get(TEST_NAME)
    assert_true(es, "Can't found energyswitch with name '%s'" % TEST_NAME)

def testES_2():
    """
    @description: [ECS.1.2] List energy switched
    @id: ECS.1.2
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitch.list()
    @expected_result: function should return a list of all energy switches in ecs
    """
    client = getClient()
    ess = client.energyswitch.list()
    found = False
    for es in ess:
        if es['energyswitchname'] == TEST_NAME and es['ipaddress'] == TEST_IP:
            found = True
            break
    
    assert_true(found, "The added energy switch was not found by list")

def testES_3():
    """
    @description: [ECS.1.3] Check if energy switch exists 
    @id: ECS.1.3
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitch.exists(id)
    @expected_result: function should return true if energyswitche with the given id is in ecs
    """
    client = getClient()
    es = client.energyswitch.get(TEST_NAME)
    assert_true(client.energyswitch.exists(es['energyswitchid']), "The created energy switch not found")

def testES_4():
    """
    @description: [ECS.1.4] Do setGroups 
    @id: ECS.1.4
    @timestamp: 1301304493
    @signature: mazmy
    @params: client.energyswitch.setGroups(id, user, restricted, admin)
    @expected_result: function should set the energyswitch groups
    """
    client = getClient()
    es = client.energyswitch.get(TEST_NAME)
    usergrp = "user_group"
    restgrp = "rest_group"
    admingrp = "admin_group"
    client.energyswitch.setGroups(es['energyswitchid'], usergrp, restgrp, admingrp)
    
    es = client.energyswitch.get(TEST_NAME)
    assert_true(es['user'] == usergrp, "User group was not set")
    assert_true(es['restricted'] == restgrp, "Restricted group was not set")
    assert_true(es['admin'] == admingrp, "Admin group was not set")
    
def testES_5():
    """
    @description: [ECS.1.5] Do setUser
    @id: ECS.1.5
    @timestamp: 1301304493
    @signature: mazmy
    @params: client.energyswitch.setUser(id, user)
    @expected_result: function should set the energyswitch user group
    """
    client = getClient()
    es = client.energyswitch.get(TEST_NAME)
    usergrp = "user_group000"
    client.energyswitch.setUser(es['energyswitchid'], usergrp)
    
    es = client.energyswitch.get(TEST_NAME)
    assert_true(es['user'] == usergrp, "User group was not set")
    
def testES_6():
    """
    @description: [ECS.1.6] Do setRestricted
    @id: ECS.1.6
    @timestamp: 1301304493
    @signature: mazmy
    @params: client.energyswitch.setRestricted(id, restricted)
    @expected_result: function should set the energyswitch restricted group
    """
    client = getClient()
    es = client.energyswitch.get(TEST_NAME)
    restgrp = "rest_group000"
    client.energyswitch.setRestricted(es['energyswitchid'], restgrp)
    
    es = client.energyswitch.get(TEST_NAME)
    assert_true(es['restricted'] == restgrp, "Restricted group was not set")

def testES_7():
    """
    @description: [ECS.1.7] Do setAdmin
    @id: ECS.1.7
    @timestamp: 1301304493
    @signature: mazmy
    @params: client.energyswitch.setAdmin(id, admin)
    @expected_result: function should set the energyswitch admin group
    """
    client = getClient()
    es = client.energyswitch.get(TEST_NAME)
    admingrp = "admin_group000"
    client.energyswitch.setAdmin(es['energyswitchid'], admingrp)
    
    es = client.energyswitch.get(TEST_NAME)
    assert_true(es['admin'] == admingrp, "Admin group was not set")
    
def testES_8():
    """
    @description: [ECS.1.8] Energyswitch delete 
    @id: ECS.1.8
    @timestamp: 1300279992
    @signature: mazmy
    @params: client.energyswitch.delete(id)
    @expected_result: function should delete an energy switch
    """
    client = getClient()
    es = client.energyswitch.get(TEST_NAME)
    client.energyswitch.delete(es['energyswitchid'])
    
    assert_false(client.energyswitch.exists(es['energyswitchid']), "energyswitch wasn't deleted successfully")

def testES_9():
    """
    @description: [ECS.1.9] Add an energy switch with user, restricted and admin set
    @id: ECS.1.9
    @timestamp: 1300279992
    @signature: rvanover
    @params: client.energyswitch.add(ip, name)
    @expected_result: function should add energy switch to ecs
    """
    client = getClient()
    client.energyswitch.add(TEST_IP, TEST_NAME, TEST_TYPE, TEST_USER, TEST_RESTRICTED, TEST_ADMIN)
    es = client.energyswitch.get(TEST_NAME)
    assert_true(es, "Can't find energyswitch with name '%s'" % TEST_NAME)
    assert_equals(es["user"], TEST_USER, "User-field should be '%s' but was '%s'" % (TEST_USER, es["user"]))
    assert_equals(es["restricted"], TEST_RESTRICTED, "Restricted-field should be '%s' but was '%s'" % (TEST_RESTRICTED, es["restricted"]))
    assert_equals(es["admin"], TEST_ADMIN, "Admin-field should be '%s' but was '%s'" % (TEST_ADMIN, es["admin"]))

def testES_10():
    """
    @description: [ECS.1.10] Update an energy switch with user, restricted and admin set
    @id: ECS.1.10
    @timestamp: 1300279992
    @signature: rvanover
    @params: client.energyswitch.add(ip, name)
    @expected_result: function should add energy switch to ecs
    """
    newName = "test_new_name"
    newIp = "1.2.3.4"
    newUser = "cn=testUser123"
    newRestricted = "cn=testRestricted123"
    newAdmin = "cn=testAdmin123"
    
    client = getClient()
    es = client.energyswitch.get(TEST_NAME)
    assert_true(es, "Can't find energyswitch with name '%s'" % TEST_NAME)
    client.energyswitch.update(str(es["energyswitchid"]), newIp, newName, TEST_TYPE, newUser, newRestricted, newAdmin)

    es = client.energyswitch.get(newName)
    assert_true(es, "Can't find energyswitch with name '%s'" % newName)
    assert_equals(es["ipaddress"], newIp, "Ipaddress-field should be '%s' but was '%s'" % (newIp, es["ipaddress"]))
    assert_equals(es["user"], newUser, "User-field should be '%s' but was '%s'" % (newUser, es["user"]))
    assert_equals(es["restricted"], newRestricted, "Restricted-field should be '%s' but was '%s'" % (newRestricted, es["restricted"]))
    assert_equals(es["admin"], newAdmin, "Admin-field should be '%s' but was '%s'" % (newAdmin, es["admin"]))

def testES_11():
    """
    @description: [ECS.1.11] Energyswitch delete 
    @id: ECS.1.11
    @timestamp: 1300279992
    @signature: rvanover
    @params: client.energyswitch.delete(id)
    @expected_result: function should delete an energy switch
    """
    newName = "test_new_name"
    client = getClient()
    es = client.energyswitch.get(newName)
    client.energyswitch.delete(es['energyswitchid'])
    
    assert_false(client.energyswitch.exists(es['energyswitchid']), "energyswitch wasn't deleted successfully")