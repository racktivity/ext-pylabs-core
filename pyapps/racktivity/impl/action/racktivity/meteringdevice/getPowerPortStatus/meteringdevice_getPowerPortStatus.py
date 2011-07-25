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
        if port.label == params['portlabel']:
            portid = port.sequence
            break
    
    if portid == None:
        events.raiseError("Can't find port sequence for a port with label '%s'" % params['portlabel'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0052', tags='', escalate=False)

    actorresult = q.actions.actor.meteringdevice.getPowerPortStatus(meteringdeviceguid, master.meteringdevicetype, master.network.ipaddress, master.network.port, meteringdevice.id, portid, master.accounts[0].login, master.accounts[0].password)['result']
    actorresult['text'] = "On" if actorresult['status'] else "Off"
    params['result'] = actorresult

def match(q, i, params, tags):
    return True

