__author__ = 'racktivity'
from logger import logger
from rootobjectaction_lib import events

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    fields = ('name', 'id', 'meteringdevicetype', 'meteringdeviceconfigstatus', 'template', 'rackguid', 'parentmeteringdeviceguid', \
              'clouduserguid', 'height', 'positionx', 'positiony', 'positionz', 'attributes', 'tags')
    objectfields = {'powerinputinfo': 'powerinputs', 'poweroutputinfo': 'poweroutputs', 'portsinfo': 'ports', 
                    'sensorinfo': 'sensors', 'accounts': 'accounts', 'nicinfo': 'nics'}
    if exists('racktivity_view_meteringdevice_list', p.api.model.racktivity.meteringdevice , "name", params['name']):
        events.raiseError("Meteringdevice with the same name already exists", messageprivate='', typeid='', tags='', escalate=False)
    
    if params["meteringdeviceconfigstatus"] != "IDENTIFIED":
        if not exists('racktivity_view_rack_list', p.api.model.racktivity.rack , "guid", params['rackguid']):
            events.raiseError("Invalid rack guid, rack doesn't exists", messageprivate='', typeid='', tags='', escalate=False)
    
    if params["nicinfo"]:
        nics = params["nicinfo"]
        for nic in nics:
            for ipguid in nic["ipaddressguids"]:
                if not exists('racktivity_view_ipaddress_list', p.api.model.racktivity.ipaddress , "guid", ipguid):
                    events.raiseError("Invalid ipaddress guid, doesn't exists", messageprivate='', typeid='', tags='', escalate=False)
    
    meteringdevice = p.api.model.racktivity.meteringdevice.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(meteringdevice, key, value)
    for info, attr in objectfields.iteritems():
        if info in params and params[info]:
            objlist = getattr(meteringdevice, attr)

            for infodict in params[info]:
                newobj = objlist.new()
                for key, value in infodict.iteritems():
                    setattr(newobj, key, value)
                objlist.append(newobj)
    acl = meteringdevice.acl.new()
    meteringdevice.acl = acl
    p.api.model.racktivity.meteringdevice.save(meteringdevice)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(meteringdevice.guid, 'meteringdevice', params['request']['username'])

    #Create MeteringdeviceAPI application for this meteringdevice
    if not meteringdevice.parentmeteringdeviceguid:
        if meteringdevice.attributes and meteringdevice.attributes['deviceapiportnr']:
            portnr = int(meteringdevice.attributes['deviceapiportnr'])
        else:
            portnr = 80
        applicationguid = p.api.action.racktivity.application.create(name='MeteringdeviceAPI', deviceguid=meteringdevice.guid, request = params["request"])['result']['applicationguid']
        application = p.api.model.racktivity.application.get(applicationguid)
        networkservice = application.networkservices.new()
        port = networkservice.ports.new()
        port.portnr = portnr
        if meteringdevice.nics and meteringdevice.nics[0].ipaddressguids:
            networkservice.ipaddressguids.append(meteringdevice.nics[0].ipaddressguids[0])
        networkservice.ports.append(port)
        application.networkservices.append(networkservice)
        p.api.model.racktivity.application.save(application)

    ismodule = params['parentmeteringdeviceguid']
    #generate UI page for master metering devices only (in case of configured or userd)
    if meteringdevice.meteringdeviceconfigstatus in (q.enumerators.meteringdeviceconfigstatus.CONFIGURED, q.enumerators.meteringdeviceconfigstatus.USED):
        parentguid = params['rackguid']
        #import racktivityui.uigenerator.meteringdevice
        #import racktivityui.uigenerator.rack
        #if not ismodule:
            #racktivityui.uigenerator.meteringdevice.create(meteringdevice.guid, parentguid)
        #else:
            #This is a module being created, update the parent page 
            #racktivityui.uigenerator.meteringdevice.update(params['parentmeteringdeviceguid'])
        #racktivityui.uigenerator.rack.update(parentguid)
    
        if not ismodule:
            q.logger.log('Creating a policy for meteringdevice %s' % meteringdevice.name, 3)
            p.api.action.racktivity.policy.create('meteringdevice_%s' % meteringdevice.name, rootobjecttype='meteringdevice', rootobjectaction='monitor',
                                               rootobjectguid=meteringdevice.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                               request = params["request"])

    #Create data stores
    #from rootobjectaction_lib import rootobjectaction_find
    #appserverguids = rootobjectaction_find.application_find(name='appserverrpc')
    #if not appserverguids:
        #raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    #appserver = p.api.model.racktivity.application.get(appserverguids[0])
    #url = appserver.networkservices[0].name

    #meteringdeviceguid = meteringdevice.guid
    
    #stores = list()
    #for sensor in meteringdevice.sensors:
        ##Create a database for the sensor humidity (meteringdeviceguid_sensorid_humidity)
        #sensorid = sensor.sequence
        #storename = str(sensor.sensortype).replace("SENSOR", "").lower()
        #stores.append('%s_%s_%s' % (meteringdeviceguid, sensorid, storename))

    #portsmtypes = ('current', 'powerfactor', 'activeenergy',
                   #'apparentenergy')
    
    #for poweroutput in meteringdevice.poweroutputs:
        #portindex = poweroutput.sequence
        #for type in portsmtypes:
            #storename = '%s_%s_%s' % (meteringdeviceguid, portindex, type)
            #stores.append(storename)

    #if meteringdevice.poweroutputs or meteringdevice.powerinputs:
        #mtypes = ('current', 'voltage', 'frequency',
                  #'activeenergy', 'apparentenergy',
                  #'powerfactor', 'temperature', 'humidity')
        #for type in mtypes:
            ##Add frequency database (meteringdeviceguid_current)
            #storename = '%s_%s' % (meteringdeviceguid, type)
            #stores.append(storename)
        
    #q.actions.actor.graphdatabase.createStores(url, stores)
    
    params['result'] = {'returncode': True, 'meteringdeviceguid': meteringdevice.guid}

def match(q, i, params, tags):
    return True
