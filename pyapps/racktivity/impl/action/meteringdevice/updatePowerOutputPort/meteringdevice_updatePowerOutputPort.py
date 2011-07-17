__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'updatePowerOutputPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    master = None
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = q.drp.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)
        
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
    
    fields = {'label': 'newportlabel', 'sequence': 'sequence', 'thresholdguids': 'thresholds', 'attributes': 'attributes'}
    for fieldkey, fieldvalue in fields.iteritems():
        if fieldvalue in params and params[fieldvalue]:
            if fieldkey == 'attributes':
                requiredpoweroutput.attributes.update(params[fieldvalue])
            else:
                setattr(requiredpoweroutput, fieldkey, params[fieldvalue])
            changed = True
    if changed:
        q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode':True}
    
    from rootobjectaction_lib import rootobjectaction_find
    applications = rootobjectaction_find.racktivity_application_find(meteringdeviceguid=master.guid, name='MeteringdeviceAPI')
    masteripaddress = None
    deviceapiport = 0
    if applications:
        racktivity_application = q.drp.racktivity_application.get(applications[0])
        service = racktivity_application.networkservices[0]
        if not  service.ipaddressguids:
            events.raiseError("Can't find ipaddress attached to this meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='', tags='', escalate=False)
        ipaddress = q.drp.ipaddress.get(service.ipaddressguids[0])
        masteripaddress = ipaddress.address
        deviceapiport = service.ports[0].portnr
    else:
        events.raiseError("Can't find racktivity_application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)
        
    if oldname != requiredpoweroutput.label:
        success = q.actions.actor.meteringdevice.setPortData(params['meteringdeviceguid'], master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, requiredpoweroutput.sequence,
                                                           'PortName', requiredpoweroutput.label, master.accounts[0].login, master.accounts[0].password)['result']['returncode']
        
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True