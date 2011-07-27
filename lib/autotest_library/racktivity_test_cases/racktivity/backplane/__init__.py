from pylabs import i,q,p
import racktivity_test_library

def setup():
    global data
    data = dict()
    data["ca"] = i.config.cloudApiConnection.find("main")

def teardown():
    pass

def getData():
    return data
