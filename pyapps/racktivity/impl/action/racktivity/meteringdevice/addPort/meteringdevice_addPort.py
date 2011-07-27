__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    for port in meteringdevice.ports:
        if port.label == params['label']:
            events.raiseError('Port label must be unique within the module', messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0044', tags='', escalate=False)

    portfields = ('label', 'porttype', 'sequence')
    port = meteringdevice.ports.new()
    for key, value in params.iteritems():
        if key in portfields and value:
            setattr(port, key, value)
    
    if not port.sequence:
        maxsequence = 0
        for p in meteringdevice.ports:
            maxsequence = max(p.sequence, maxsequence)
        port.sequence = maxsequence + 1
    
    if port.sequence <= 0:
        events.raiseError("Sequence must be 1 or more", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0045', tags='', escalate=False)
    
    #validate the sequence and the label
    for p in meteringdevice.ports:
        if port.sequence == p.sequence:
            events.raiseError("Sequence '%s' is already taken by another port" % port.sequence, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0046', tags='', escalate=False)
        
    meteringdevice.ports.append(port)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}



def match(q, i, params, tags):
    return True