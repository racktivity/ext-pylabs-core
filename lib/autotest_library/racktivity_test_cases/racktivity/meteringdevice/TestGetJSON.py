from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid, getEmulatorConfig

EMPTY_GUID = '00000000-0000-0000-0000-000000000000'
METERINGDEVICE_NAME = 'test-racktivitydevice'
IPADDRESS_NAME = 'test-localip'
mdguid = pmguid = ipaddress = None


def getCloudapi():
    return p.api.action.racktivity

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def getPowerModuleGuid():
    global pmguid
    return pmguid

def getIPAddress():
    global ipaddress
    return ipaddress

def setup():
    global mdguid, pmguid, ipaddress
    ipaddress,port,type = getEmulatorConfig()
    mdguid, pmguid = racktivity_test_library.meteringdevice.createRacktivity(METERINGDEVICE_NAME, getRackGuid(),
                                                                   ipaddress=ipaddress,
                                                                   meteringdevicetype=type,
                                                                   port=port)
    
    
def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())

def testGetJSON_1():
    """
    @description: [0.16.20.01] Test Get Json data from meteringdevice
    @id: 0.16.20.01
    @timestamp: 1293360398
    @signature: mina_magdy
    @params: cloudapi.meteringdevice.getCurrentDeviceData(guid, 'all')
    @expected_result: All the metering device data are found
    """
    ip,port,type = getEmulatorConfig()
    cloudapi = getCloudapi()
    result = cloudapi.meteringdevice.getJSON(getMeteringdeviceGuid())['result']
    import json
    result = json.loads(result)
    md = cloudapi.meteringdevice.getObject(getMeteringdeviceGuid())
    assert_equals(md.rackguid, result["rackguid"])
    assert_equals(md.clouduserguid, result["clouduserguid"])
    assert_equals(md.name, result["name"])
    assert_equals(str(md.meteringdeviceconfigstatus), result["meteringdeviceconfigstatus"])
    assert_equals(result["ipaddress"], ip)
    assert_equals(md.id, result["id"])

def testGetJSON_2():
    """
    @description: [0.16.20.02] Test Get Json data from empty meteringdevice
    @id: 0.16.20.01
    @timestamp: 1293360398
    @signature: mina_magdy
    @params: cloudapi.meteringdevice.getCurrentDeviceData(guid, 'all')
    @expected_result: All the metering device data are found
    """
    cloudapi = getCloudapi()
    mdguid = cloudapi.meteringdevice.create("MyMD", "M1", "PM0816", None, "00000000-0000-0000-0000-000000000000", meteringdeviceconfigstatus="IDENTIFIED" )["result"]["meteringdeviceguid"]
    result = cloudapi.meteringdevice.getJSON(mdguid)['result']
    cloudapi.meteringdevice.delete(mdguid)
    import json
    result = json.loads(result)
    assert_equals("00000000-0000-0000-0000-000000000000", result["rackguid"])
    assert_equals("MyMD", result["name"])
    assert_equals("IDENTIFIED", result["meteringdeviceconfigstatus"])
    assert_equals(result["ipaddress"], None)
    assert_equals("M1", result["id"])
