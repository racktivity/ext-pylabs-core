__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    for port in meteringdevice.ports:
        if port.label == params['label']:
            raise ValueError('Port label must be unique within the module')

    portfields = ('label', 'porttype', 'sequence')
    port = meteringdevice.ports.new()
    for key, value in params.iteritems():
        if key in portfields and value:
            setattr(port, key, value)
    
    if not port.sequence:
        maxsequence = 0
        for pt in meteringdevice.ports:
            maxsequence = max(pt.sequence, maxsequence)
        port.sequence = maxsequence + 1
    
    if port.sequence <= 0:
        raise ValueError("Sequence must be 1 or more")
    
    #validate the sequence and the label
    for pt in meteringdevice.ports:
        if port.sequence == pt.sequence:
            raise ValueError("Sequence '%s' is already taken by another port")
        
    meteringdevice.ports.append(port)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}



def match(q, i, params, tags):
    return True
