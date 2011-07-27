from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = i.config.cloudApiConnection.find("main")

def getData():
    return data
