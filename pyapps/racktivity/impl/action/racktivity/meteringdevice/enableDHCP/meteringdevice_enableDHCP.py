__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    changed = False
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    nics = meteringdevice.nics
    if len(nics) >= 1:
        nic = nics[0]
        if len(nic.ipaddressguids) >= 1:
            ipaddressguid = nic.ipaddressguids[0]
            ipaddress = p.api.model.racktivity.ipaddress.get(ipaddressguid)
            ipaddress.iptype = q.enumerators.iptype.DHCP
            changed = True
    if changed:
        p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True