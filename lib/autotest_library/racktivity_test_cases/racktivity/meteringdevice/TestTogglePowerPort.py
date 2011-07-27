from nose.tools import *
from xmlrpclib import Fault
import racktivity_test_library
from pylabs import i,q,p
from . import getRackGuid, getEmulatorConfig

EMPTY_GUID = '00000000-0000-0000-0000-000000000000'
METERINGDEVICE_NAME = 'test-racktivitydevice'
IPADDRESS_NAME = 'test-localip'
PORT_LABEL = 'output-1'
mdguid = pmguid = ipaddressguid = None

def getCloudapi():
    return p.api.action.racktivity

def getMeteringdeviceGuid():
    global mdguid
    return mdguid

def getPowerModuleGuid():
    global pmguid
    return pmguid

def getIPAddressGuid():
    global ipaddressguid
    return ipaddressguid

def setup():
    global mdguid, pmguid, ipaddressguid
    ip,port,type = getEmulatorConfig()
    ipaddressguid = racktivity_test_library.ipaddress.create(IPADDRESS_NAME, ip)
    mdguid, pmguid = racktivity_test_library.meteringdevice.createRacktivity(METERINGDEVICE_NAME, getRackGuid(),
                                                                   ipaddressguid=ipaddressguid,
                                                                   meteringdevicetype=type,
                                                                   port=port)

def teardown():
    racktivity_test_library.meteringdevice.delete(getMeteringdeviceGuid())

def testTogglePowerPort():
    """
    @description: [0.16.23.01] Test Power Togle Power Port
    @id: 0.16.23.01
    @timestamp: 1306310584
    @signature: kneirinc
    @params: cloudapi.meteringdevice.togglePowerPort(guid, label)
    @expected_result: The port status is toggled from OFF to ON to OFF again

    """
    cloudapi = getCloudapi()

    startstatus = None
    status1 = None
    status2 = None
    startstatus = cloudapi.meteringdevice.getPowerPortStatus(getPowerModuleGuid(), PORT_LABEL)['result']['status']
    cloudapi.meteringdevice.togglePowerPort(getPowerModuleGuid(), PORT_LABEL)
    status1 = cloudapi.meteringdevice.getPowerPortStatus(getPowerModuleGuid(), PORT_LABEL)['result']['status']
    cloudapi.meteringdevice.togglePowerPort(getPowerModuleGuid(), PORT_LABEL)
    status2 = cloudapi.meteringdevice.getPowerPortStatus(getPowerModuleGuid(), PORT_LABEL)['result']['status']

    assert_not_equal(status1, startstatus, "Port status didn't change after first toggle")
    assert_not_equal(status1, status2, "Port status didn't change after second toggle")
    assert_equal(status2, startstatus, "Port status failed to change during one of the toggles")


