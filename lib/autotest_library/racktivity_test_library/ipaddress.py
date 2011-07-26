from pymonkey import q, i

def create(name = "test_ipaddress", address='127.0.0.1', netmask='255.0.0.0', iptype='STATIC', ipversion='IPV4'):
    cloudapi = i.config.cloudApiConnection.find('main')
    guid = cloudapi.ipaddress.create(name, address=address, netmask=netmask, iptype=iptype, ipversion=ipversion)['result']['ipaddressguid']
    ipaddress = cloudapi.ipaddress.getObject(guid)
    if ipaddress.address != address:
        raise RuntimeError("IPAddress '%s' didn't create properly" % guid)
    return guid

def delete(guid):
    cloudapi = i.config.cloudApiConnection.find('main')
    cloudapi.ipaddress.delete(guid)
    ips = cloudapi.ipaddress.list(ipaddressguid=guid)['result']['ipaddressinfo']
    if ips:
        raise RuntimeError("IPAddress '%s' didn't delete properly")
    