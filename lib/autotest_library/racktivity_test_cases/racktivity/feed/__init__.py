from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = p.api.action.racktivity
    data["dcguid"] = racktivity_test_library.datacenter.create()

def teardown():
    racktivity_test_library.datacenter.delete(data["dcguid"], delLocation = True)

def getData():
    return data
