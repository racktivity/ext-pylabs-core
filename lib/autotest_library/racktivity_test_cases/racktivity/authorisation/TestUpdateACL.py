from nose.tools import *
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

def testUpdateACL_1():
    """
    @description: add a group to the acl list on a specific action for a location, and then update the acl and check
    @id: 0090903
    @timestamp: 1293360198
    @signature: rami
    @params: ca.location.UpdateACL(locationguid, {})
    @expected_result: the cloudusergroupnames should be an empty dict
    """
    assert_true(ca.location.addGroup(locationguid, cloudusergroupguid, action='delete')['result']['returncode'], msg="The addGroup function failed")
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_true(cloudusergroupactions.find(cloudusergroupguid+"_delete") >= 0, msg="The group was not added")
    ca.location.updateACL(locationguid, cloudusergroupnames={})
    cloudusergroupactions = ca.location.list(locationguid=locationguid)['result']['locationinfo'][0]['cloudusergroupactions']
    assert_false(cloudusergroupactions.find(cloudusergroupguid+"_delete") >= 0, msg="The ACL was not updated successfully")
