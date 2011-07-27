from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = p.api.action.racktivity

def teardown():
    pass

def getData():
    return data
