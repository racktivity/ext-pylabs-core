from pymonkey import q, i
import racktivity_test_library

DATACENTER_NAME = 'dc-test-meteringdevice'
FLOOR_NAME = 'floor-test-meteringdevice'
ROOM_NAME = 'room-test-meteringdevice'
RACK_NAME = 'rack-test-meteringdevice'

dcguid = roomguid = rackguid = emulatorip = emulatorport = emulatortype = None

def getDatacenterGuid():
    global dcguid
    return dcguid

def getRoomGuid():
    global roomguid
    return roomguid

def getRackGuid():
    global rackguid
    return rackguid

def getEmulatorConfig():
    global emulatorip, emulatorport, emulatortype
    if not emulatorip:
        cfg = q.config.getConfig('emulatoraddress')
        if 'main' in cfg:
            emulatorip = cfg['main']['ipaddress']
            emulatorport = int(cfg['main'].get('port', 7654))
            emulatortype = cfg['main'].get('type', 'racktivity')
        else:
            emulatorip = '127.0.0.1'
            emulatorport = 7654
            emulatortype = 'racktivity'
    
    return emulatorip, emulatorport, emulatortype

def setup():
    racktivity_test_library.cleanenv()
    global dcguid, roomguid, rackguid
    dcguid = racktivity_test_library.datacenter.create(DATACENTER_NAME)
    floorguid = racktivity_test_library.floor.create(FLOOR_NAME, dcguid)
    roomguid = racktivity_test_library.room.create(ROOM_NAME, dcguid, floorguid)
    rackguid = racktivity_test_library.rack.create(RACK_NAME, roomguid)

def teardown():
    racktivity_test_library.datacenter.delete(getDatacenterGuid(), delLocation=True)