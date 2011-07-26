from pymonkey import q, i

def getCloudApi():
    global ca
    return ca

def setup():
    global ca
    ca =  i.config.cloudApiConnection.find('main')
