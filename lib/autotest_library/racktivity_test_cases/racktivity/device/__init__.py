from pylabs import q, i
import racktivity_test_library

DATACENTER_NAME = 'dc-test-device'
FLOOR_NAME = 'floor-test-device'
ROOM_NAME = 'room-test-device'
RACK_NAME = 'rack-test-device'

dcguid = roomguid = rackguid = None

def getDatacenterGuid():
    global dcguid
    return dcguid

def getRoomGuid():
    global roomguid
    return roomguid

def getRackGuid():
    global rackguid
    return rackguid

def setup():
    racktivity_test_library.cleanenv()
    global dcguid, roomguid, rackguid
    dcguid = racktivity_test_library.datacenter.create(DATACENTER_NAME)
    floorguid = racktivity_test_library.floor.create(FLOOR_NAME, dcguid)
    roomguid = racktivity_test_library.room.create(ROOM_NAME, dcguid, floorguid)
    rackguid = racktivity_test_library.rack.create(RACK_NAME, roomguid)

def teardown():
    global dcguid
    racktivity_test_library.datacenter.delete(dcguid,delLocation=True)