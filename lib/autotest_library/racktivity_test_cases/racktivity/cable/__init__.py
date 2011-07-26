from pymonkey import i
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = i.config.cloudApiConnection.find("main")

def teardown():
    pass

def getData():
    return data
