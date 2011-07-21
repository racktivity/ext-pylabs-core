__author__ = 'racktivity'
from logger import logger

def getMacRange(q):
    macranges = []
    newMac = ''
    for lan in p.api.action.racktivity.lan.list()['result']['laninfo']:
        if lan['macrange']:
            macrange = '0x' + lan['macrange'].replace(':', '')
            macranges.append(int(macrange, 0))
    macranges.sort()
    if macranges:
        newMac = hex(macranges[-1] + 1).replace('x', '')
        numberOfInserts = len(newMac)/2 -1
    counter = 1
    mac = ''
    for char in newMac:
        mac = mac + str(char)
        if counter % 2 == 0:
            mac = mac + ':'
        counter = counter + 1
    return mac.rstrip(':')

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    from pylabs.pmtypes import IPv4Address, IPv4Range

    #Check if another datacenter with the same name already exist
    if exists('racktivity_view_lan_list', p.api.model.racktivity.lan, "name", params['name']):
        raise ValueError("Lan with the same name already exists")
    #Calculate non given parameters
    network = params['network']
    netmask = params['netmask']
    startip = params['fromip'] or str(IPv4Address(network) + 1)
    endip = params['toip'] or str(IPv4Address((~int(IPv4Address(netmask))) | int(IPv4Address(network))) + (-1))
    #Validate Start/End ip
    net = IPv4Range(netIp=network, netMask=netmask)
    ip1 = IPv4Address(startip)
    ip2 = IPv4Address(endip)
    assert(ip1 in net)
    assert(ip2 in net)
    assert(ip1 < ip2)
    #Carry on with the creation process
    lan = p.api.model.racktivity.lan.new()
    lan.vlantag = 0
    lan.status = q.enumerators.lanstatustype.NOTCONNECTED

    for key, value in {'network':network, 'netmask':netmask, 'startip':startip, 'endip':endip}.iteritems():
        setattr(lan, key, value)
    for field in ('name', 'gateway', 'parentlanguid', 'backplaneguid', 'lantype', 'description', 'tags'):
        setattr(lan, field, params[field])
    
    if params['dns']:
        for dnsip in params['dns']:
            dns = lan.dns.new()
            dns.ip = dnsip
            lan.dns.append(dns)

    backplane = p.api.model.racktivity.backplane.get(params['backplaneguid'])
    lan.managementflag = False
    lan.publicflag = backplane.publicflag
    lan.storageflag = False
    lan.macrange = getMacRange(q)
    acl = lan.acl.new()
    lan.acl = acl
    p.api.model.racktivity.lan.save(lan)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(lan.guid, 'lan', params['request']['username'])

    if lan.lantype == q.enumerators.lantype.DYNAMIC: 
        #Check if the IP address exists, otherwise create it
        filterObject = p.api.model.racktivity.ipaddress.getFilterObject()
        filterObject.add('racktivity_view_ipaddress_list', 'address', startip)
        addressfound = len(p.api.model.racktivity.ipaddress.find(filterObject)) > 0
        if not addressfound:
            p.api.action.racktivity.ipaddress.create(name=startip, address=startip, netmask=netmask, iptype=q.enumerators.iptype.STATIC, ipversion=q.enumerators.ipversion.IPV4, \
                                                      languid=lan.guid, request = params["request"], executionparams={"description":"Creating ipaddress"})

    p.api.action.racktivity.lan.setStatus(languid=lan.guid, status=str(q.enumerators.lanstatustype.ACTIVE), request = params["request"])
    params['result'] = {'returncode': True,
                        'languid': lan.guid}

def match(q, i, params, tags):
    return True
