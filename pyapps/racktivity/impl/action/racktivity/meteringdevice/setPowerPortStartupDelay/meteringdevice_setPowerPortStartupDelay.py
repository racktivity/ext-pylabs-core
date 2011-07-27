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
        events.raiseError("Could not find powerport with label %s" % label, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0053', tags='', escalate=False)
    
    result = p.api.actor.meteringdevice.setPowerPortStartupDelay(meteringdeviceguid, master.meteringdevicetype, master.network.ipaddress, master.network.port, meteringdevice.id, portid,
                                                           params['delay'], master.accounts[0].login, master.accounts[0].password)['result']
    params['result'] = {'returncode':result}

def match(q, i, params, tags):
    return True