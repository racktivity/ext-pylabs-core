__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'addOutputPowerPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
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
    q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name
    
    portsmtypes = ('current', 'powerfactor', 'activeenergy',
                   'apparentenergy')
    
    portindex = poweroutput.sequence
    meteringdeviceguid = meteringdevice.guid
    
    stores = list()
    for type in portsmtypes:
        storename = '%s_%s_%s' % (meteringdeviceguid, portindex, type)
        stores.append(storename)
            
    q.actions.actor.graphdatabase.createStores(url, stores)

    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True