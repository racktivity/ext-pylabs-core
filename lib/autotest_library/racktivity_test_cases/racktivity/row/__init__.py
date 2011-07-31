from pylabs import i,q,p
import racktivity_test_library

def setup():
    global data
    racktivity_test_library.cleanenv()
    data = dict()
    data["ca"] = p.api.action.racktivity
    data["dc1"] = racktivity_test_library.datacenter.create()
    data['floorguid'] = racktivity_test_library.floor.create('test_floor1', data["dc1"])
    data["room1"] = racktivity_test_library.room.create("test_room1", data["dc1"], data['floorguid'])
    data["pod1"] = racktivity_test_library.pod.create(data["room1"], "test_pod1")

def teardown():
    racktivity_test_library.datacenter.delete(data["dc1"], delLocation = True)

def getData():
    return data
