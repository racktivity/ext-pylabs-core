__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    poweroutputs = meteringdevice.poweroutputs
    for poweroutput in poweroutputs:
        if poweroutput.label == params['label']:
            events.raiseError('Output power port label must be unique within the module', messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0035', tags='', escalate=False)

    fields = ('label', 'sequence')
    poweroutput = meteringdevice.poweroutputs.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(poweroutput, key, value)
    
    if not poweroutput.sequence:
        maxsequence = 0
        for output in meteringdevice.poweroutputs:
            maxsequence = max(output.sequence, maxsequence)
        poweroutput.sequence = maxsequence + 1

    if poweroutput.sequence <= 0:
        events.raiseError("Sequence must be 1 or more", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0036', tags='', escalate=False)
    
    #validate the sequence and the label
    for output in meteringdevice.poweroutputs:
        if poweroutput.sequence == output.sequence:
            events.raiseError("Sequence '%s' is already taken by another port" % powerinput.sequence, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0037', tags='', escalate=False)
    
    
    meteringdevice.poweroutputs.append(poweroutput)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}


    portsmtypes = ('current', 'powerfactor', 'activeenergy',
                   'apparentenergy')
    
    portindex = poweroutput.sequence
    meteringdeviceguid = meteringdevice.guid
    
    stores = list()
    for type in portsmtypes:
        storename = '%s_%s_%s' % (meteringdeviceguid, portindex, type)
        stores.append(storename)
            
    q.actions.actor.graphdatabase.createStores(stores)


def match(q, i, params, tags):
    return True