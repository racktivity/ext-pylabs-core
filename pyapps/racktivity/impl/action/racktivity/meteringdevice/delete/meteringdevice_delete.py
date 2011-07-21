__author__ = 'racktivity'
from logger import logger

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    q.logger.log('Deleting metering device %s' % meteringdeviceguid)
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)

    #Disconnect poweroutput and powerinput ports on the meteringdevice
    q.logger.log('Disconnecting powerinput and poweroutput ports', 3)
    for powerinput in meteringdevice.powerinputs:
        if powerinput.cableguid:
            p.api.action.racktivity.meteringdevice.disconnectPowerInputPort(meteringdeviceguid, portlabel=powerinput.label, request = params["request"])
    for poweroutput in meteringdevice.poweroutputs:
        if poweroutput.cableguid:
            p.api.action.racktivity.meteringdevice.disconnectPowerOutputPort(meteringdeviceguid, portlabel=poweroutput.label, request = params["request"])

    q.logger.log('Deleting children of the meteringdevice', 3)
    filterObject = p.api.model.racktivity.meteringdevice.getFilterObject()
    filterObject.add('racktivity_view_meteringdevice_list', 'parentmeteringdeviceguid', meteringdeviceguid)
    children = p.api.model.racktivity.meteringdevice.find(filterObject)
    #children = p.api.action.racktivity.meteringdevice.find(parentmeteringdeviceguid=meteringdeviceguid)['result']['guidlist']
    for child in children:
        p.api.action.racktivity.meteringdevice.delete(child, request = params["request"])

    #Delete the policy linked to this meteringdevice
    q.logger.log('Deleting policies linked to this meteringdevice', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=meteringdeviceguid)
    for policyguid in  policyguids:
        p.api.model.racktivity.policy.delete(policyguid)

    #q.logger.log('Deleting stores', 3)
    #appserverguids = rootobjectaction_find.application_find(name='appserverrpc')
    #if not appserverguids:
        #raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    #appserver = p.api.model.racktivity.application.get(appserverguids[0])
    #url = appserver.networkservices[0].name
        
    #stores = []
    #portsmtypes = ('current', 'powerfactor', 'activeenergy',
                   #'apparentenergy')
    #for poweroutput in meteringdevice.poweroutputs:
        #portindex = poweroutput.sequence
        #for type in portsmtypes:
            #stores.append('%s_%s_%s' % (meteringdeviceguid, portindex, type))
    
    #for sensor in meteringdevice.sensors:
        #dbname = str(sensor.sensortype).replace("SENSOR", "").lower()
        #stores.append('%s_%s_%s' % (meteringdeviceguid, sensor.sequence, dbname))
        
    #if meteringdevice.poweroutputs or meteringdevice.powerinputs:
        #mtypes = ('current', 'voltage', 'frequency',
                  #'activeenergy', 'apparentenergy', 
                  #'powerfactor', 'temperature', 'humidity')
        #for type in mtypes:
            #stores.append('%s_%s' % (meteringdeviceguid, type))
        
    #q.actions.actor.graphdatabase.destroyStores(url, stores)

    #if not meteringdevice.parentmeteringdeviceguid:
        #q.logger.log('Deleting the MeteringdeviceAPI application', 3)
        #applications = rootobjectaction_find.application_find(meteringdeviceguid = meteringdeviceguid, name="MeteringdeviceAPI")
        #if applications:
            #applicationguid = applications[0]
            #p.api.action.racktivity.application.delete(applicationguid, request = params["request"])
    
    #Delete the ipaddress attached to this meteringdevice
    q.logger.log('Deleting ipaddresses attached to the meteringdevice', 3)
    for nic in meteringdevice.nics:
        for ipaddressguid in nic.ipaddressguids:
            try:
                p.api.model.racktivity.ipaddress.get(ipaddressguid)
            except:
                continue
            p.api.action.racktivity.ipaddress.delete(ipaddressguid, request = params["request"])
    
    params['result'] = {'returncode': p.api.model.racktivity.meteringdevice.delete(meteringdeviceguid)}

    #Delete the meteringdevice page and update the rack page
    if meteringdevice.meteringdeviceconfigstatus in (q.enumerators.meteringdeviceconfigstatus.CONFIGURED, q.enumerators.meteringdeviceconfigstatus.USED):
        q.logger.log('Deleting the meteringdevice page and updating the rack page with new information', 3)
        #import racktivityui.uigenerator
        #racktivityui.uigenerator.deletePage(meteringdeviceguid)
        #if meteringdevice.parentmeteringdeviceguid:
            #import racktivityui.uigenerator.meteringdevice
            #racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid)
        #else:
            #import racktivityui.uigenerator.rack
            #racktivityui.uigenerator.rack.update(meteringdevice.rackguid)

def match(q, i, params, tags):
    return True