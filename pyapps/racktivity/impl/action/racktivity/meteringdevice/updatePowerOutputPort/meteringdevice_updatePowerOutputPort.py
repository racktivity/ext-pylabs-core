__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    master = None
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)
        
    changed = False
    requiredpoweroutput = None

    for poweroutput in meteringdevice.poweroutputs:
        if poweroutput.label == params['portlabel']:
            requiredpoweroutput = poweroutput
        elif poweroutput.label == params['newportlabel']:
            events.raiseError('Label must be unique within the module', messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0071', tags='', escalate=False)
        elif poweroutput.sequence == params['sequence']:
            events.raiseError('Sequence must be unique within the module', messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0072', tags='', escalate=False)

    if not requiredpoweroutput:
        events.raiseError('Could not find a power output port with label "%s" in module "%s"' % (params['portlabel'], meteringdevice.name), messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0058', tags='', escalate=False)

    oldname = requiredpoweroutput.label
    
    fields = {'label': 'newportlabel', 'sequence': 'sequence', 'attributes': 'attributes'}
    for fieldkey, fieldvalue in fields.iteritems():
        if fieldvalue in params and params[fieldvalue]:
            if fieldkey == 'attributes':
                requiredpoweroutput.attributes.update(params[fieldvalue])
            else:
                setattr(requiredpoweroutput, fieldkey, params[fieldvalue])
            changed = True
    if changed:
        p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode':True}
    
    if oldname != requiredpoweroutput.label:
        success = p.api.actor.meteringdevice.setPortData(params['meteringdeviceguid'], master.meteringdevicetype, master.network.ipaddress, master.network.port, meteringdevice.id, requiredpoweroutput.sequence,
                                                           'PortName', requiredpoweroutput.label, master.accounts[0].login, master.accounts[0].password)['result']['returncode']

def match(q, i, params, tags):
    return True
