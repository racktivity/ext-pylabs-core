from pylabs import q, i

def getCloudApi():
    global ca
    return ca

def setup():
    global ca
    ca = p.api.action.racktivity
