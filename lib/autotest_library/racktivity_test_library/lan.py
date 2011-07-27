from pymonkey import q, i
import backplane

def create(name, backplaneguid, lantype = 'STATIC', network="192.168.20.0", netmask="255.255.255.0", gateway="192.168.20.1"):
    ca = i.config.cloudApiConnection.find('main')
    if not backplaneguid:
        backplaneguid = backplane.create()
    guid = ca.lan.create(backplaneguid, name, lantype,network=network, netmask=netmask, gateway=gateway)['result']['languid']
    lan = ca.lan.getObject(guid)
    if lan.network != network:
        raise RuntimeError("lan '%s' was not created properly" % guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find('main')
    ca.lan.delete(guid)
    lans = ca.lan.list(languid=guid)['result']['laninfo']
    if lans:
        raise RuntimeError("lan '%s' was not deleted properly")