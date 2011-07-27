from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = i.config.cloudApiConnection.find("main")
    data["dcguid"] = racktivity_test_library.datacenter.create()
    data['floorguid'] = racktivity_test_library.floor.create('test_floor1', data["dcguid"])
    data["roomguid"] = racktivity_test_library.room.create("test_room1", data["dcguid"], data['floorguid'])

def teardown():
    racktivity_test_library.datacenter.delete(data["dcguid"], delLocation = True)

def getData():
    return data
