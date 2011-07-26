from pymonkey import i
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = i.config.cloudApiConnection.find("main")
    data["dcguid"] = racktivity_test_library.datacenter.create()

def teardown():
    racktivity_test_library.datacenter.delete(data["dcguid"], delLocation = True)

def getData():
    return data
