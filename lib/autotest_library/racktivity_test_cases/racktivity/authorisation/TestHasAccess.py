from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q,p

def setup():
    global cloudusergroupguid
    cloudusergroupguid = racktivity_test_library.cloudusergroup.create(name='test_cloudusergroup1')
    global locationguid
    locationguid = racktivity_test_library.location.create(name='test_location1')
    global datacenterguid
    datacenterguid = racktivity_test_library.datacenter.create(name='test_datacenter1', locationguid=locationguid)
    global ca
    ca = p.api.action.racktivity

def teardown():
    racktivity_test_library.cloudusergroup.delete(cloudusergroupguid)
    racktivity_test_library.location.delete(locationguid)

def testHasAccess_1():
    """
    @description: add a group to the acl list on a specific action for a location, and then call hasAccess to validate that the group has access on the child datacenter
    @id: 0090903
    @timestamp: 1293360198
    @signature: rami
    @params: ca.datacenter.hasAccess(datacenterguid, [clouduserguid], action)
    @expected_result: function should return True
    """
    assert_true(ca.location.addGroup(locationguid, cloudusergroupguid, action='delete', recursive=True)['result']['returncode'], msg="The addGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_delete") >= 0, msg="The group was not added")
    assert_true(ca.datacenter.hasAccess(datacenterguid, [cloudusergroupguid], action="delete")['result']['returncode'], 'The cloudusergroup does not have access on the child datacenter')

def testHasAccess_2():
    """
    @description: delete a group from the acl list on an actions for a location, and then call hasAccess to validate that the group does not have access on the child datacenter
    @id: 0090904
    @timestamp: 1293360198
    @signature: rami
    @params:ca.datacenter.hasAccess(datacenterguid, [clouduserguid], action)
    @expected_result: function should return False
    """
    assert_true(ca.location.addGroup(locationguid, cloudusergroupguid, action='delete', recursive=True)['result']['returncode'], msg="The addGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_true(cloudusergroupactions.index(cloudusergroupguid+"_delete") >= 0, msg="The group was not added")
    assert_true(ca.location.deleteGroup(locationguid, cloudusergroupguid, action='delete', recursive=True), msg="The deleteGroup function failed")
    assert_false(ca.datacenter.hasAccess(datacenterguid, [cloudusergroupguid], action='delete')['result']['returncode'], 'The cloudusergroup still has access on the child datacenter')

