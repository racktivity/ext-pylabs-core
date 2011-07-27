__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    port = None
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    
    for poweroutput in meteringdevice.poweroutputs:
        if poweroutput.label == params['label']:
            port = poweroutput
            break
    
    if not port:
        events.raiseError("No port found with name '%s'" % params['label'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0041', tags='', escalate=False)

    portsmtypes = ('current', 'powerfactor', 'activeenergy',
                   'apparentenergy')
    
    databasenames = []
    for type in portsmtypes:
        databasenames.append('%s_%s_%s' % (meteringdeviceguid, port.sequence, type))
    
    p.api.actor.racktivity.graphdatabase.destroyStores(databasenames)

    meteringdevice.poweroutputs.remove(port)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode':True}



def match(q, i, params, tags):
    return True