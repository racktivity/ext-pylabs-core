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

def testDeleteGroup_1():
    """
    @description: add a group to the acl list on a specific action for a location, and then delete it
    @id: 0090903
    @timestamp: 1293360198
    @signature: rami
    @params: ca.location.deleteGroup(locationguid, clouduserguid, action)
    @expected_result: function should delete the group guid from the acl list for this action
    """
    assert_true(ca.location.addGroup(locationguid, cloudusergroupguid, action='delete')['result']['returncode'], msg="The addGroup function failed")
    assert_true(ca.location.deleteGroup(locationguid, cloudusergroupguid, action='delete'), msg="The deleteGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_false(cloudusergroupactions.find(cloudusergroupguid+"_delete") >= 0, msg="The group was not deleted")

def testDeleteGroup_2():
    """
    @description: delete a group from the acl list on all actions for a location
    @id: 0090904
    @timestamp: 1293360198
    @signature: rami
    @params:ca.location.deleteGroup(locationguid, clouduserguid)
    @expected_result: function should delete the group guid from the acl list for all actions
    """
    assert_true(ca.location.addGroup(locationguid, cloudusergroupguid)['result']['returncode'], msg="The addGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_create") >= 0, msg="The group was not added")
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_delete") >= 0, msg="The group was not added")
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_getObject") >= 0, msg="The group was not added")
    assert_true(ca.location.deleteGroup(locationguid, cloudusergroupguid), msg="The deleteGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_false(cloudusergroupactions.find(cloudusergroupguid+"_delete") >= 0, msg="The group was not deleted")
    assert_false(cloudusergroupactions.find(cloudusergroupguid+"_create") >= 0, msg="The group was not deleted")
    assert_false(cloudusergroupactions.find(cloudusergroupguid+"_getObject") >= 0, msg="The group was not deleted")
