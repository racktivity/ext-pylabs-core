from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = p.api.action.racktivity
    data["backplaneguid1"] = racktivity_test_library.backplane.create('backplane_test1')
    data["backplaneguid2"] = racktivity_test_library.backplane.create('backplane_test2')

def teardown():
    racktivity_test_library.backplane.delete(data["backplaneguid1"])
    racktivity_test_library.backplane.delete(data["backplaneguid2"])

def getData():
    return data
