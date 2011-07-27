from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p

def setup():
    global cloudusergroupguid
    cloudusergroupguid = racktivity_test_library.cloudusergroup.create(name='test_cloudusergroup1')
    global locationguid
    locationguid = racktivity_test_library.location.create(name='test_location1')
    global ca
    ca = p.api.action.racktivity

def teardown():
    racktivity_test_library.cloudusergroup.delete(cloudusergroupguid)
    racktivity_test_library.location.delete(locationguid)

def testAddGroup_1():
    """
    @description: add a group to the acl list on a specific action for a location
    @id: 0090901
    @timestamp: 1293360198
    @signature: rami
    @params: ca.location.addGroup(locationguid, clouduserguid, action)
    @expected_result: function should add the group guid to the acl list for this action
    """
    assert_true(ca.location.addGroup(locationguid, cloudusergroupguid, action='delete')['result']['returncode'], msg="The addGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_delete") >= 0, msg="The group was not added")

def testAddGroup_2():
    """
    @description: add a group to the acl list on all actions for a location
    @id: 0090902
    @timestamp: 1293360198
    @signature: rami
    @params:ca.location.addGroup(locationguid, clouduserguid)
    @expected_result: function should add the group guid to the acl list for all actions
    """
    assert_true(ca.location.addGroup(locationguid, cloudusergroupguid)['result']['returncode'], msg="The addGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_create") >= 0, msg="The group was not added")
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_delete") >= 0, msg="The group was not added")
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_getObject") >= 0, msg="The group was not added")

