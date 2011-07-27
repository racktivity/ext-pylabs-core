from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    global data
    data = dict()
    data["ca"] = p.api.action.racktivity
    data["locGuid1"] = racktivity_test_library.location.create("test_location1")
    data["locGuid2"] = racktivity_test_library.location.create("test_location2")
    data["usrGuid1"] = racktivity_test_library.clouduser.create('test_user1')
    data["usrGuid2"] = racktivity_test_library.clouduser.create('test_user2')

def teardown():
    racktivity_test_library.location.delete(data["locGuid1"])
    racktivity_test_library.location.delete(data["locGuid2"])
    racktivity_test_library.clouduser.delete(data["usrGuid1"])
    racktivity_test_library.clouduser.delete(data["usrGuid2"])

def getData():
    return data
