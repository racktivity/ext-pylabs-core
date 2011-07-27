from pylabs import i,q,p
import racktivity_test_library

def setup():
    global data
    racktivity_test_library.cleanenv()
    data = dict()
    data["ca"] = p.api.action.racktivity
    data["dcguid"] = racktivity_test_library.datacenter.create()
    data['floorguid'] = racktivity_test_library.floor.create("floor-test-room1", data["dcguid"])

def teardown():
    racktivity_test_library.datacenter.delete(data["dcguid"], delLocation = True)

def getData():
    return data
