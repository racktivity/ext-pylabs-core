__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'disableDHCP'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    changed = False
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    nics = meteringdevice.nics
    if len(nics) >= 1:
        nic = nics[0]
        if len(nic.ipaddressguids) >= 1:
            ipaddressguid = nic.ipaddressguids[0]
            ipaddress = q.drp.ipaddress.get(ipaddressguid)
            ipaddress.iptype = q.enumerators.iptype.STATIC
            changed = True
    if changed:
        q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True