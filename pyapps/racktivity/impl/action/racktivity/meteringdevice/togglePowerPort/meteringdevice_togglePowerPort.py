__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)

    portid = None
    for port in meteringdevice.poweroutputs:
        if port.label == params['label']:
            portid = port.sequence
            break

    if portid == None:
        raise ValueError("Could not find powerport with label %s" % label)

    masteripaddress = master.network.ipaddress
    deviceapiport = master.network.port
    result = p.api.actor.racktivity.meteringdevice.getPowerPortStatus(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, portid, master.accounts[0].login, master.accounts[0].password)['result']
    if (result['status']):
        p.api.actor.racktivity.meteringdevice.powerOffPowerPort(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, portid, master.accounts[0].login, master.accounts[0].password)
    else:
        p.api.actor.racktivity.meteringdevice.powerOnPowerPort(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, portid, master.accounts[0].login, master.accounts[0].password)
    params['result'] = {'returncode':True, 'portStatus':not result['status']}

def match(q, i, params, tags):
    return True
