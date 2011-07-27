from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = p.api.action.racktivity
    backplaneguid = racktivity_test_library.backplane.create("test_backplane1")
    data['backplainGuid'] = backplaneguid
    data["lanGuid1"] = racktivity_test_library.lan.create("test_lan1", backplaneguid)
    data["lanGuid2"] = racktivity_test_library.lan.create("test_lan2", backplaneguid)

def teardown():
    racktivity_test_library.lan.delete(data["lanGuid1"])
    racktivity_test_library.lan.delete(data["lanGuid2"])
    racktivity_test_library.backplane.delete(data['backplainGuid'])

def getData():
    return data