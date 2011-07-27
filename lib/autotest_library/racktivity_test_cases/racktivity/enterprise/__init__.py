from pylabs import i,q,p
import racktivity_test_library

def setup():
    racktivity_test_library.cleanenv()
    cloudapi = p.api.action.racktivity
    for enter in cloudapi.enterprise.find()['result']['guidlist']:
        cloudapi.enterprise.delete(enter)

def teardown():
    #restore all deleted enterprise.
    cloudapi = p.api.action.racktivity
    cloudapi.enterprise.create("enterprise")