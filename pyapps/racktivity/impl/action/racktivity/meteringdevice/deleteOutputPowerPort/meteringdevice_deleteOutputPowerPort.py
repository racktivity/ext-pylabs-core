__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'deleteOutputPowerPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    port = None
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    
    for poweroutput in meteringdevice.poweroutputs:
        if poweroutput.label == params['label']:
            port = poweroutput
            break
    
    if not port:
        events.raiseError("No port found with name '%s'" % params['label'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0041', tags='', escalate=False)

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name

    portsmtypes = ('current', 'powerfactor', 'activeenergy',
                   'apparentenergy')
    
    databasenames = []
    for type in portsmtypes:
        databasenames.append('%s_%s_%s' % (meteringdeviceguid, port.sequence, type))
    
    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

    meteringdevice.poweroutputs.remove(port)
    q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode':True}

    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True