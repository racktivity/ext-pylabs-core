from pymonkey import q, i
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    cloudapi = i.config.cloudApiConnection.find("main")
    for guid in cloudapi.enterprise.find()['result']['guidlist']:
        try:
            cloudapi.enterprise.delete(guid)
        except:
            pass
    
    cloudapi.enterprise.create("enterprise")
    
def teardown():
    cloudapi = i.config.cloudApiConnection.find("main")
    for guid in cloudapi.enterprise.find()['result']['guidlist']:
        cloudapi.enterprise.delete(guid)