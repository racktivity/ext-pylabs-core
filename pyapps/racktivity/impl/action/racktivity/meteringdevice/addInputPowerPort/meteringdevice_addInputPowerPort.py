__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    powerinputs = meteringdevice.powerinputs
    for powerinput in powerinputs:
        if powerinput.label == params['label']:
            raise ValueError("Input power port label must be unique within the module")

    fields = ('label', 'sequence')
    powerinput = meteringdevice.powerinputs.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(powerinput, key, value)
            
    if not powerinput.sequence:
        maxsequence = 0
        for input in meteringdevice.powerinputs:
            maxsequence = max(input.sequence, maxsequence)
        powerinput.sequence = maxsequence + 1
    
    if powerinput.sequence <= 0:
        raise ValueError("Sequence must be 1 or more")
    
    #validate the sequence and the label
    for input in meteringdevice.powerinputs:
        if powerinput.sequence == input.sequence:
            raise ValueError("Sequence '%s' is already taken by another port" % powerinput.sequence)
            
    meteringdevice.powerinputs.append(powerinput)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode':True}


def match(q, i, params, tags):
    return True
