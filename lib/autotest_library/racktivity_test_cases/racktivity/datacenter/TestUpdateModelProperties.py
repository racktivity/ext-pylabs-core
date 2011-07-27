from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import racktivity_test_library
from . import getData

def setup():
    global ca, locGuid1, locGuid2, usrGuid1, usrGuid2, dc1Guid
    data = getData()
    ca = p.api.action.racktivity
    locGuid1 = data["locGuid1"]
    locGuid2 = data["locGuid2"]
    usrGuid1 = data["usrGuid1"]
    usrGuid2 = data["usrGuid2"]
    dc1Guid = racktivity_test_library.datacenter.create('test_DataCenter1', locGuid1, clouduserguid = usrGuid1)

def teardown():
    racktivity_test_library.datacenter.delete(dc1Guid)

def testUpdate_1():
    """
    @description: [0081701] Updating datacenter name
    @id: 0081701
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.updateModelProperties(dc1Guid, name = "test_DataCenter_rename")
    @expected_result: datacenter name should be updated
    """
    q.logger.log("         Updating datacenter name")
    ca.datacenter.updateModelProperties(dc1Guid, name = "test_DataCenter_rename")
    dc1 = ca.datacenter.getObject(dc1Guid)
    racktivity_test_library.ui.doUITest("Real+time+data", "UPDATE", value=dc1.name)
    ok_(racktivity_test_library.ui.getResult( dc1.name))

def testUpdate_2():
    """
    @description: [0081702] Updating datacenter description
    @id: 0081702
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.updateModelProperties(dc1Guid, description = "test_DataCenter_rename")
    @expected_result: datacenter description should be updated
    """
    q.logger.log( "         Updating datacenter description")
    ca.datacenter.updateModelProperties(dc1Guid, description = "test_DataCenter_rename")

def testUpdate_3():
    """
    @description: [0081703] Updating datacenter locationguid
    @id: 0081703
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.updateModelProperties(dc1Guid, locationguid = locGuid2)
    @expected_result: datacenter locationguid should be updated
    """
    q.logger.log( "         Updating datacenter locationguid")
    ca.datacenter.updateModelProperties(dc1Guid, locationguid = locGuid2)

def testUpdate_4():
    """
    @description: [0081704] Updating datacenter clouduserguid
    @id: 0081704
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.updateModelProperties(dc1Guid, clouduserguid = usrGuid2)
    @expected_result: datacenter clouduserguid should be updated
    """
    q.logger.log("         Updating datacenter clouduserguid")
    ca.datacenter.updateModelProperties(dc1Guid, clouduserguid = usrGuid2)

@raises(xmlrpclib.Fault)
def testUpdate_5():
    """
    @description: [0081705] Updating datacenter with nonexisting locationguid
    @id: 0081705
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.updateModelProperties(dc1Guid, locationguid = '00000000-0000-0000-0000-000000000000')
    @expected_result: datacenter update should fail because locationguid is invalid
    """
    q.logger.log("         Updating datacenter with nonexisting locationguid")
    ca.datacenter.updateModelProperties(dc1Guid, locationguid = '00000000-0000-0000-0000-000000000000')
    #If that worked, I shouldn't leave it like that
    ca.datacenter.updateModelProperties(dc1Guid, locationguid = locGuid)

@raises(xmlrpclib.Fault)
def testUpdate_6():
    """
    @description: [0081706] Updating datacenter with nonexisting clouduserguid
    @id: 0081706
    @timestamp: 1293360198
    @signature: mmagdy
    @params: ca.datacenter.updateModelProperties(dc1Guid, clouduserguid = '00000000-0000-0000-0000-000000000000')
    @expected_result: datacenter update should fail because clouduserguid is invalid
    """
    q.logger.log("         Updating datacenter with nonexisting clouduserguid")
    ca.datacenter.updateModelProperties(dc1Guid, clouduserguid = '00000000-0000-0000-0000-000000000000')
    #If that worked, I shouldn't leave it like that
    ca.datacenter.updateModelProperties(dc1Guid, clouduserguid = usrGuid)

