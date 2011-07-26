from pymonkey import i
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    cloudapi = i.config.cloudApiConnection.find("main")
    for enter in cloudapi.enterprise.find()['result']['guidlist']:
        cloudapi.enterprise.delete(enter)

def teardown():
    #restore all deleted enterprise.
    cloudapi = i.config.cloudApiConnection.find("main")
    cloudapi.enterprise.create("enterprise")