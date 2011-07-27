from nose.tools import *
from pylabs import q, i
import racktivity_test_library

DATACENTER_NAME = 'dc-test-export'
FLOOR_NAME = 'floor-test-export'
ROOM_NAME = 'room-test-export'
RACK_NAME = 'rack-test-export'
IPADDRESS_NAME = 'ipaddress-test-export'
METERINGDEVICE_NAME = 'md-test-exoort'

LOGICALVIEW_NAME= "logicalview-test-export"
LOGICALVIEW_QUERY = "types:{datacenter}"

dcguid = roomguid = rackguid = mdguid = pmguid = ipaddressguid = logicalviewguid = emulatorip = None

global request
request = {'username':'admin', 'ipaddress':'127.0.0.1'}

def getRequest():
    global request
    request = {'username':'admin', 'ipaddress':'127.0.0.1'}
    return request

def getCloudapi():
    return p.api.action.racktivity

def getDatacenterGuid():
    global dcguid
    return dcguid

def getRoomGuid():
    global roomguid
    return roomguid

def getRackGuid():
    global rackguid
    return rackguid

def getMeteringDeviceGuid():
    global mdguid
    return mdguid

def getLogicalViewGuid():
    global logicalviewguid
    return logicalviewguid

def getEmulatorAddress():
    global emulatorip
    if not emulatorip:
        cfg = q.config.getConfig('emulatoraddress')
        if 'main' in cfg:
            emulatorip = cfg['main']['ipaddress']
        else:
            emulatorip = '127.0.0.1'
    
    return emulatorip

def setup():
    racktivity_test_library.cleanenv()
    global dcguid, roomguid, rackguid, mdguid, pmguid, ipaddressguid, logicalviewguid
    
    dcguid = racktivity_test_library.datacenter.create(DATACENTER_NAME)
    floorguid = racktivity_test_library.floor.create(FLOOR_NAME, dcguid)
    roomguid = racktivity_test_library.room.create(ROOM_NAME, dcguid, floorguid)
    rackguid = racktivity_test_library.rack.create(RACK_NAME, roomguid)
    ipaddressguid = racktivity_test_library.ipaddress.create(IPADDRESS_NAME, getEmulatorAddress())
    mdguid, pmguid = racktivity_test_library.meteringdevice.createRacktivity(METERINGDEVICE_NAME, getRackGuid(),
                                                                   ipaddressguid=ipaddressguid,
                                                                   port=7654)
    cloudapi = getCloudapi()
    logicalviewguid = cloudapi.logicalview.create(LOGICALVIEW_NAME, LOGICALVIEW_QUERY)['result']['logicalviewguid']

def teardown():
    cloudapi = getCloudapi()
    cloudapi.logicalview.delete(getLogicalViewGuid())
    racktivity_test_library.cleanenv()
    