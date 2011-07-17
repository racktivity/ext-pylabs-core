__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'addPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
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
    q.drp.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True