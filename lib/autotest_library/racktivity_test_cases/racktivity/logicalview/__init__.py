from pymonkey import i
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = i.config.cloudApiConnection.find("main")
    data["loc"] = racktivity_test_library.location.create("MainLoc", tags="Cairo Egypt company:Info")
    data["dc1"] = racktivity_test_library.datacenter.create("DC1", data["loc"], tags="first datacenter location:Giza")
    data["dc2"] = racktivity_test_library.datacenter.create("DC2", data["loc"], tags="second datacenter location:Cairo")
    data["floorguid"] = racktivity_test_library.floor.create("FLOOR", data["dc1"])
    data["roomguid"] = racktivity_test_library.room.create("ROOM", data["dc1"], data["floorguid"])
    data["rackguid"] = racktivity_test_library.rack.create("RACK", data["roomguid"])
    data["mdguid1"] = racktivity_test_library.meteringdevice.create("MD1", 'M1', data["rackguid"])
    data["mdguid2"] = racktivity_test_library.meteringdevice.create("MD2", 'M1', data["rackguid"])
    data["mdguid3"] = racktivity_test_library.meteringdevice.create("MD3", 'M1', data["rackguid"])
    
def teardown():
    ca = data["ca"]
    ca.location.delete(data["loc"])

def getData():
    return data
