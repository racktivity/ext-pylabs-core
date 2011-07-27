from pylabs import i,q,p
import racktivity_test_library

DATACENTER_NAME = 'dc-test-meteringdevice'
FLOOR_NAME = 'floor-test-meteringdevice'
ROOM_NAME = 'room-test-meteringdevice'
RACK_NAME = 'rack-test-meteringdevice'

def setup():
    racktivity_test_library.cleanenv()
    global dcguid, roomguid, rackguid
    dcguid = racktivity_test_library.datacenter.create(DATACENTER_NAME)
    floorguid = racktivity_test_library.floor.create(FLOOR_NAME, dcguid)
    roomguid = racktivity_test_library.room.create(ROOM_NAME, dcguid, floorguid)
    rackguid = racktivity_test_library.rack.create(RACK_NAME, roomguid)

    global data
    data = dict()
    data["ca"] = p.api.action.racktivity
    data["devGuid1"] = racktivity_test_library.device.create("test_device1", rackguid)
    data["devGuid2"] = racktivity_test_library.device.create("test_device2", rackguid)

def teardown():
    global dcguid
    racktivity_test_library.datacenter.delete(dcguid)

def getData():
    return data
