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
        events.raiseError("Can't find port sequence for a port with label '%s'" % params['portlabel'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0079', tags='', escalate=False)

    result = p.api.actor.meteringdevice.getPortData(meteringdeviceguid, master.meteringdevicetype, master.network.ipaddress, master.network.port, meteringdevice.id, portid, params['meteringtype'], master.accounts[0].login, master.accounts[0].password)
    params['result'] = result['result']
  

def match(q, i, params, tags):
    return True

