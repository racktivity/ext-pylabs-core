from pylabs import q,p

def exists(view, obj, key, value):
    """
    This function determine if the "value" of the attribute "key" in onject "obj" exists or not
    Usually used to prevent creation of two objects with the same name
    sample usage: exists('racktivity_view_location_list', p.api.model.racktivity.location, "name", params['name'])
    """
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def acl_find(rootobjecttype, rootobjectguid=""):
    params={'rootobjecttype':rootobjecttype, 'rootobjectguid':rootobjectguid}
    filterObject = p.api.model.racktivity.acl.getFilterObject()
    view = 'racktivity_view_acl_list'
    for key,value in params.iteritems():
        if value:
            filterObject.add(view, key, value)
    result = p.api.model.racktivity.acl.find(filterObject)
    return result

def application_find(deviceguid="", meteringdeviceguid="", name="",status="", tags=""):
    params={'deviceguid':deviceguid, 'meteringdeviceguid':meteringdeviceguid, 'name':name, 'status':status, 'tags':tags}
    filterObject = p.api.model.racktivity.application.getFilterObject()
    for param in params.iterkeys():
        if params[param] not in (None, ''):
            filterObject.add('racktivity_view_application_list', param , params[param])
    result = p.api.model.racktivity.application.find(filterObject)
    return result

def backplane_find(name="", managementflag="", publicflag="", storageflag="", backplanetype="", tags=""):
    view =  'racktivity_view_backplane_list'
    filterObject = p.api.model.racktivity.backplane.getFilterObject()
    params={'name':name, 'managementflag':managementflag, 'storageflag':storageflag, 'backplanetype':backplanetype, 'tags':tags}
    for key, value in params.iteritems():
        if value:
            filterObject.add(view, key, value)
    result = p.api.model.racktivity.backplane.find(filterObject)
    return result

def cable_find(name="", cabletype="", description="", label="", tags=""):
    view =  'racktivity_view_cable_list'
    params={'name':name, 'cabletype':cabletype, 'description':description, 'label':label, 'tags':tags}
    filterObject = p.api.model.racktivity.cable.getFilterObject()
    for key, value in params.iteritems():
        if value:
            filterObject.add(view, key, value)
    result = p.api.model.racktivity.cable.find(filterObject)
    return result

def clouduser_find(login="", email="", name="", status="", tags=""):
    view = 'racktivity_view_clouduser_list'
    params={'login':login, 'email':email, 'name':name, 'status':status, 'tags':tags}
    filterObject = p.api.model.racktivity.clouduser.getFilterObject()
    for key, value in params.iteritems():
        if value:
            filterObject.add(view, key, value)    
    result = p.api.model.racktivity.clouduser.find(filterObject)
    return result

def cloudusergroup_find(name="", tags=""):
    filterObject = p.api.model.racktivity.cloudusergroup.getFilterObject()
    view = 'racktivity_view_cloudusergroup_list'
    params = {'name': name, 'tags': tags}
    for key, value in params.iteritems():
        if value:
            filterObject.add(view, key, value)
    result = p.api.model.racktivity.cloudusergroup.find(filterObject)
    return result

def customer_find(name="", status="", tags=""):
    filterObject = p.api.model.racktivity.customer.getFilterObject()
    view = 'racktivity_view_customer_list'
    params={'name':name, 'status':status, 'tags':tags}
    for key,value in params.iteritems():
        if value:
            filterObject.add(view, key, value)
    result = p.api.model.racktivity.customer.find(filterObject)
    return result

def datacenter_find(name="",  description="", locationguid="", clouduserguid="", tags=""):
    params = {'name':name, 'description':description, 'locationguid':locationguid, 'clouduserguid':clouduserguid, 'tags':tags}
    view = 'racktivity_view_datacenter_list'
    filterObject = p.api.model.racktivity.datacenter.getFilterObject()
    for key,value in params.iteritems():
        if value:
            filterObject.add(view, key, value)
    result = p.api.model.racktivity.datacenter.find(filterObject)
    return result

def device_find(name="", macaddress="", status="", devicetype="", description="", template="", modelnr="",serialnr="",firmware="", \
                rackguid="",datacenterguid="", parentdeviceguid="",cableguid="", tags=""):
    filterObject = p.api.model.racktivity.device.getFilterObject()
    params = {'name': name, 'macaddress':macaddress, 'cableguid':cableguid, 'status':status, 'devicetype':devicetype, 'description':description,\
              'template':template, 'modelnr':modelnr, 'serialnr':serialnr, 'firmware':firmware, 'rackguid':rackguid, 'datacenterguid':datacenterguid, \
              'parentdeviceguid':parentdeviceguid, 'tags':tags}
    defaultview = 'racktivity_view_device_list'
    viewmap = {"macaddress": 'racktivity_view_device_nicports', "cableguid": "view_device_powerports"}
    for key,value in params.iteritems():
        if value:
            viewName = viewmap.get(key, defaultview)
            filterObject.add(viewName, key, value)
    result = p.api.model.racktivity.device.find(filterObject)
    return result

def errorcondition_find(errorconditiontype="", timestamp="", level="", agent="", tags=[], application=""):
    filterObject = p.api.model.racktivity.errorcondition.getFilterObject()
    params = {'errorconditiontype':errorconditiontype, 'timestamp':timestamp, 'level':level, 'agent':agent, 'tags':tags, 'application':application}
    view = 'racktivity_view_errorcondition_list'
    for key,value in params.iteritems():
        if value:
            filterObject.add(view, key, value)
    result = p.api.model.racktivity.errorcondition.find(filterObject)    
    return result

def ipaddress_find(name="", description="", address="", netmask="",block = False, iptype="", ipversion="", languid="", cloudspaceguid="", virtual=None, tags=""):
    view = 'racktivity_view_ipaddress_list'
    blockval = 'f'
    if block:
        blockval = 't'
    params={'name':name, 'description':description, 'address':address, 'netmask':netmask, 'block':blockval, 'iptype':iptype, 'ipversion':ipversion, \
            'languid':languid, 'cloudspaceguid':cloudspaceguid, 'virtual':virtual, 'tags':tags}
    filterObject = p.api.model.racktivity.ipaddress.getFilterObject()
    for key,value in params.iteritems():
        if value:
            if key == 'address':
                filterObject.add(view, key, value, exactMatch=True)
            else:
                filterObject.add(view, key, value)
    result = p.api.model.racktivity.ipaddress.find(filterObject)
    return result

def lan_find(backplaneguid="", name="", status="", startip="", endip="", gateway="", managementflag="", publicflag="", storageflag="", \
             network="", netmask="", parentlanguid="", vlantag="", lantype="", dhcpflag="", tags=""):
    filterObject = p.api.model.racktivity.lan.getFilterObject()
    params = {'backplaneguid':backplaneguid, 'name':name, 'status':status, 'startip':startip, 'endip':endip, 'gateway':gateway, \
              'managementflag':managementflag, 'publicflag':publicflag, 'storageflag':storageflag, 'network':network, 'netmask':netmask, \
              'parentlanguid':parentlanguid, 'vlantag':vlantag, 'lantype':lantype, 'dhcpflag':dhcpflag, 'tags':tags}
    for key, value in params.iteritems():
        if value:
            filterObject.add('racktivity_view_lan_list', key, value)
    result = p.api.model.racktivity.lan.find(filterObject)
    return result

def location_find(name="", description="", alias="", address="", city="", country="", public=False, tags=""):
    filterObject = p.api.model.racktivity.location.getFilterObject()
    params = {'name':name, 'description':description, 'alias':alias, 'address':address, 'city':city, 'country':country, 'public':public, 'tags':tags}
    for key,value in params.iteritems():
        if value:
            filterObject.add('racktivity_view_location_list', key, value)
    result = p.api.model.racktivity.location.find(filterObject)
    return result

def logicalview_find(name="", clouduserguid="", share="", tags=""):
    filterObject = p.api.model.racktivity.logicalview.getFilterObject()
    params = {'name':name, 'clouduserguid':clouduserguid, 'share':share, 'tags':tags}
    for key, value in params.iteritems():
        if value:
            filterObject.add('racktivity_view_logicalview_list', key, value)
    result = p.api.model.racktivity.logicalview.find(filterObject)
    return result


def meteringdevice_find(name="", id="", meteringdevicetype="", template=False, rackguid="", parentmeteringdeviceguid="", clouduserguid="", \
                        height=0, positionx=0, positiony=0, positionz=0,  cableguid="", thresholdguid="", ipaddressguid="", tags="", meteringdeviceconfigstatus=""):
    
    params = {'name':name, 'id':id, 'meteringdevicetype':meteringdevicetype, 'template':template, 'thresholdguid':thresholdguid, \
              'rackguid':rackguid, 'cableguid':cableguid, 'parentmeteringdeviceguid':parentmeteringdeviceguid, \
              'clouduserguid':clouduserguid, 'height':height, 'positionx':positionx, 'positiony':positiony, \
              'positionz':positionz, 'ipaddressguid':ipaddressguid, 'tags':tags, 'meteringdeviceconfigstatus': meteringdeviceconfigstatus}
    
    filterobj = p.api.model.racktivity.meteringdevice.getFilterObject()
    defaultview = 'racktivity_view_meteringdevice_list'
    viewmap = {"cableguid": "racktivity_view_meteringdevice_poweroutput", 'thresholdguid': 'view_meteringdevice_thresholds', 'ipaddressguid': 'view_meteringdevice_ipaddresses'}
    for key, value in params.iteritems():
        if value:
            view = viewmap.get(key, defaultview)
            filterobj.add(view, key, value)
    result = p.api.model.racktivity.meteringdevice.find(filterobj)
    return result

def meteringdeviceevent_find(meteringdeviceguid="", portsequence="", sensorsequence="", eventtype="", level="", thresholdguid="", latest="", tags=""):
    filterObject = p.api.model.racktivity.meteringdeviceevent.getFilterObject()
    params = {'eventtype':eventtype, 'level':level, 'meteringdeviceguid':meteringdeviceguid, 'portsequence':portsequence, \
              'sensorsequence':sensorsequence, 'thresholdguid':thresholdguid, 'latest':latest, 'tags':tags}

    for key, value in params.iteritems():
        if value:
            filterObject.add('racktivity_view_meteringdeviceevent_list', key, value)
    result = p.api.model.racktivity.meteringdeviceevent.find(filterObject)
    return result

def monitoringinfo_find(monitoringinfoguid="", tags=""):
    view =  'racktivity_view_monitoringinfo_find'
    filterObj = p.api.model.racktivity.monitoringinfo.getFilterObject()
    if monitoringinfoguid:
        filterObj.add(view, 'monitoringinfoguid', monitoringinfoguid)
    moninfos = p.api.model.racktivity.monitoringinfo.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for moninfo in moninfos:
        result = dict()
        for key in moninfo.iterkeys():
            if key not in removekeys:
                result[key] = moninfo[key]
        results.append(result)
    return results

def policy_find(name="", description="", rootobjecttype="", rootobjectaction="", rootobjectguid="", interval="", tags=""):
    params = {'name':name, 'description':description, 'rootobjecttype':rootobjecttype, 'rootobjectaction':rootobjectaction, \
              'rootobjectguid':rootobjectguid, 'interval':interval, 'tags':tags}
    view = 'racktivity_view_policy_list'
    filterobj = p.api.model.racktivity.policy.getFilterObject()
    for key, value in params.iteritems():
        if value:
            filterobj.add(view, key, value)
    result = p.api.model.racktivity.policy.find(filterobj)
    return result

def resourcegroup_find(name="", customerguid="", description="", deviceguid=""):
    params = {'name': name,
              'description': description,
              'device': deviceguid}
    
    filterobj = p.api.model.racktivity.resourcegroup.getFilterObject()
    defaultview = 'racktivity_view_resourcegroup_list'
    viewmap = {"device": "racktivity_view_resourcegroup_device"}
    if customerguid:
        customer = None
        try:
            customer = p.api.model.racktivity.customer.get(customerguid)
        except:
            pass
        if customer and customer.resourcegroupguid:
            params['guid'] = customer.resourcegroupguid
        else:
            return list()
        
    for key, value in params.iteritems():
        if value:
            view = viewmap.get(key, defaultview)
            filterobj.add(view, key, value)
    results = p.api.model.racktivity.resourcegroup.find(filterobj)
    return results


def rack_find(name="", racktype="", description="", roomguid="", floor="", corridor="", position="", height="", tags=""):
    params = {'name':name, 'racktype':racktype, 'description':description, 'roomguid':roomguid, 'floor':floor, \
              'corridor':corridor, 'position':position, 'height':height, 'tags':tags}
    filterobj = p.api.model.racktivity.rack.getFilterObject()
    for key, value in params.iteritems():
        if value:
            filterobj.add('racktivity_view_rack_list', key, value)
    result = p.api.model.racktivity.rack.find(filterobj)
    return result

def room_find(name="", description="", datacenterguid="", floor="", alias="", tags=""):
    params = {'name':name, 'description':description, 'datacenterguid':datacenterguid, 'floor':floor, 'alias':alias, 'tags':tags}
    view = 'racktivity_view_room_list'
    filterobj = p.api.model.racktivity.room.getFilterObject()
    for key, value in params.iteritems():
        if value:
            filterobj.add(view, key, value)
    result = p.api.model.racktivity.room.find(filterobj)
    return result

def floor_find(name="", datacenterguid="", floor=None, alias="", tags=""):
    params = {'name': name,
              'datacenterguid': datacenterguid,
              'floor': floor,
              'alias': alias,
              'tags': tags}
    view = 'racktivity_view_floor_list'
    filterobj = p.api.model.racktivity.room.getFilterObject()
    for key, value in params.iteritems():
        if value not in [None, ""]:
            filterobj.add(view, key, value)
    
    result = p.api.model.racktivity.floor.find(filterobj)
    return result

def threshold_find(thresholdtype="", thresholdimpacttype="", tags=""):
    params = {'thresholdtype':thresholdtype, 'thresholdimpacttype':thresholdimpacttype, 'tags':tags}
    view = 'racktivity_view_threshold_list'
    filterobj = p.api.model.racktivity.threshold.getFilterObject()
    for key, value in params.iteritems():
        if value:
            filterobj.add(view, key, value)
    result = p.api.model.racktivity.threshold.find(filterobj)
    return result

def job_find(actionname="", deviceguid ="", agentguid="",applicationguid="",datacenterguid="",fromTime="",toTime="",clouduserguid=""):
    params = {'actionname':actionname, 'deviceguid':deviceguid, 'agentguid':agentguid,'applicationguid':applicationguid,'datacenterguid':datacenterguid, \
              'fromTime':fromTime, 'toTime':toTime, 'clouduserguid':clouduserguid}
    baseQuery = 'select guid as jobguid, clouduserguid, rootobjectguid, description, parentjobguid, viewguid,\
                 jobstatus, "version", rootobjecttype, actionname, agentguid, starttime, endtime, "name" from job.view_job_list'
    conditionQuery = list()
    filters = {'racktivity_view_job_list': ['name', 'actionname', 'description', 'jobstatus', 'agentguid', 'clouduserguid',
                                 'applicationguid', 'datacenterguid', 'deviceguid', 'fromTime', 'toTime', 'parentjobguid']}
    filterOptions = {'fromTime' :   ['starttime','>= '],
                     'toTime'   :   ['endtime','<= ']}
    roMapping = {'applicationguid':'application', 'datacenterguid':'datacenter', 'deviceguid':'device'}

    for filterName, filterKeys in filters.iteritems():
        for filterType in filterKeys:
            if filterType in params and params[filterType] not in ('', 0):
                if filterType in roMapping:
                    conditionQuery.append("rootobjectguid = '%s'"%params[filterType])
                    conditionQuery.append("rootobjecttype = '%s'"%roMapping[filterType])
                else:
                    conditionQuery.append("%s %s '%s'"%(filterType if filterType not in filterOptions else filterOptions[filterType][0],
                                                        '=' if filterType not in filterOptions else filterOptions[filterType][1],
                                                        params[filterType]))
    if conditionQuery:
        baseQuery += ' where %s'%' AND '.join(conditionQuery)
    baseQuery += ' order by starttime desc'
    return p.api.model.racktivity.job.query(baseQuery)

def feed_find(name="", datacenterguid="", feedproductiontype="", cableguid="", tags=""):
    params = {'name':name, 'datacenterguid':datacenterguid, 'feedproductiontype':feedproductiontype, 'cableguid':cableguid, 'tags':tags}
    defaultview = 'racktivity_view_feed_list'
    viewmap = {'cableguid': 'racktivity_view_feed_feedconnectors'}
    filterobj = p.api.model.racktivity.feed.getFilterObject()
    for key, value in params.iteritems():
        if value:
            viewName = viewmap.get(key, defaultview)
            filterobj.add(viewName, key, value)
    result = p.api.model.racktivity.feed.find(filterobj)
    return result

def enterprise_find(name="", campus="", tags=""):
    params = {'name':name, 'campus': campus, 'tags':tags}
    defaultview = 'racktivity_view_enterprise_list'
    viewmap = {'campus': 'racktivity_view_enterprise_campus'}
    filterobj = p.api.model.racktivity.enterprise.getFilterObject()

    for key, value in params.iteritems():
        if value:
            view = viewmap.get(key, defaultview)
            filterobj.add(view, key, value)

    result = p.api.model.racktivity.enterprise.find(filterobj)
    return result

def pod_find(name="", alias="", room="", rack="", tags=""):
    params = {'name':name, 'alias':alias, 'room':room, 'rack': rack, 'tags':tags}
    defaultview = 'racktivity_view_pod_list'
    viewmap = {'rack': 'racktivity_view_pod_rack'}
    filterobj = p.api.model.racktivity.pod.getFilterObject()
    for key, value in params.iteritems():
        if value:
            viewame = viewmap.get(key, defaultview)
            filterobj.add(viewame, key, value)
    result = p.api.model.racktivity.pod.find(filterobj)
    return result

def row_find(name="", alias="", room="", pod="", rack="", tags=""):
    params = {'name':name, 'alias':alias, 'rack': rack, 'room':room, 'pod':pod, 'tags':tags}
    defaultview = 'racktivity_view_row_list'
    viewmap = {'rack': 'racktivity_view_row_rack'}
    filterobj = p.api.model.racktivity.row.getFilterObject()
    for key, value in params.iteritems():
        if value:
            viewname = viewmap.get(key, defaultview)
            filterobj.add(viewname, key, value)
    result = p.api.model.racktivity.row.find(filterobj)
    return result

def autodiscoverysnmpmap_find(manufacturer=None, sysobjectid=None,tags=None):
    params = {'manufacturer':manufacturer, "sysobjectid":sysobjectid, 'tags':tags}
    defaultview = 'racktivity_view_autodiscoverysnmpmap_list'
    filterobj = p.api.model.racktivity.autodiscoverysnmpmap.getFilterObject()
    for key, value in params.iteritems():
        if value is not None:
            filterobj.add(defaultview, key, value, exactMatch=True)
    result = p.api.model.racktivity.autodiscoverysnmpmap.find(filterobj)
    return result

