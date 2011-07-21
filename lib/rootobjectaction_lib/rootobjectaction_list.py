from pylabs import q,p

def acl_list():
    filterObj = p.api.model.racktivity.acl.getFilterObject()
    acls = p.api.model.racktivity.acl.findAsView(filterObj, 'racktivity_view_acl_list')
    removekeys = ('viewguid', 'version')
    results = list()
    for acl in acls:
        result = dict()
        for key in acl.iterkeys():
            if key not in removekeys:
                result[key] = acl[key]
        results.append(result)
    return results

def application_list(deviceguid="", meteringdeviceguid="",  applicationguid="", name="",status=""):
    params = [deviceguid, meteringdeviceguid, applicationguid, name, status]
    filterObject = p.api.model.racktivity.application.getFilterObject()
    filters = {'applicationguid    ':   'guid',
               'status'             :   'status',
               'name'               :   'name',
               'deviceguid'         :   'deviceguid',
               'meteringdeviceguid' :   'meteringdeviceguid'}
    for param in filters.iterkeys():
        if param in params and not params[param] in (None, ''):
            filterObject.add('racktivity_view_application_list', filters[param] , params[param])
            
    result = p.api.model.racktivity.application.findAsView(filterObject,'racktivity_view_application_list')
    return result

def backplane_list(backplaneguid=""):
    view =  'racktivity_view_backplane_list'
    filterObj = p.api.model.racktivity.backplane.getFilterObject()
    if backplaneguid:
        filterObj.add(view, 'guid', backplaneguid)

    backplanes = p.api.model.racktivity.backplane.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version', 'guid')
    results = list()
    for backplane in backplanes:
        result = dict()
        for key in backplane.iterkeys():
            if key not in removekeys:
                result[key] = backplane[key]
        result['backplaneguid'] = backplane['guid']
        results.append(result)

    return results

def cable_list(cableguid=""):
    view =  'racktivity_view_cable_list'
    filterObj = p.api.model.racktivity.cable.getFilterObject()
    if cableguid:
        filterObj.add(view, 'guid', cableguid)
    cables = p.api.model.racktivity.cable.findAsView(filterObj, view)
    keys = ['guid','name','description','cabletype','label', 'cloudusergroupactions']
    results = list()
    for cable in cables:
        result = dict()
        for key in cable.iterkeys():
            if key in keys:
                if key == 'guid':
                    result['cableguid'] = cable['guid']
                else:
                    result[key] = cable[key]
        results.append(result)
    return results

def clouduser_list(clouduserguid=""):
    view =  'racktivity_view_clouduser_list'
    filterObj = p.api.model.racktivity.clouduser.getFilterObject()
    if clouduserguid:
        filterObj.add(view, 'guid', clouduserguid)
    cloudusers = p.api.model.racktivity.clouduser.findAsView(filterObj, view)
    removekeys = ('viewguid','version')
    results = list()
    groupquery = """
    select distinct groups.guid, groups.name from cloudusergroup.view_cloudusergroup_clouduser_list as groups
    where clouduserguid = '%s'
    """
    
    for clouduser in cloudusers:
        result = dict()
        for k in clouduser.iterkeys():
            if k not in removekeys:
                result[k] = clouduser[k]
        result['groups'] = p.api.model.racktivity.cloudusergroup.query(groupquery % result['guid'])
        results.append(result)
    return results

def cloudusergroup_list(customerguid="", cloudusergroupguid=""):
    view =  'racktivity_view_cloudusergroup_list'
    params={'guid':cloudusergroupguid, 'customerguid':customerguid}
    filterObj = p.api.model.racktivity.cloudusergroup.getFilterObject()
    for key, value in params.iteritems():
        if value:
            filterObj.add(view, key, value)

    cloudusergroups = p.api.model.racktivity.cloudusergroup.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for cloudusergroup in cloudusergroups:
        result = dict()
        for key in cloudusergroup.iterkeys():
            if key not in removekeys:
                result[key] = cloudusergroup[key]
        results.append(result)
    return results

def customer_list(customerguid=""):
    filterObj = p.api.model.racktivity.customer.getFilterObject()
    if customerguid:
        filterObj.add('racktivity_view_customer_list', 'guid', customerguid)
    customers = p.api.model.racktivity.customer.findAsView(filterObj, 'racktivity_view_customer_list')
    q.logger.log("Found '%s' customer" % len(customers))
    keys = ['guid','name','description','address','city','country','status','retentionpolicyguid','registered', 'cloudusergroupactions']
    results = list()
    for customer in customers:
        result = dict()
        for k in customer.iterkeys():
            if k in keys:
                result[k] = customer[k]
        results.append(result)
    return results

def datacenter_list(datacenterguid=""):
    view =  'racktivity_view_datacenter_list'
    filterObj = p.api.model.racktivity.datacenter.getFilterObject()
    if datacenterguid:
        filterObj.add(view, 'guid', datacenterguid)
    datacenters = p.api.model.racktivity.datacenter.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for datacenter in datacenters:
        result = dict()
        for key in datacenter.iterkeys():
            if key not in removekeys:
                result[key] = datacenter[key]
                
        results.append(result)
    return results

def device_list(deviceguid=""):
    view =  'racktivity_view_device_list'
    filterObj = p.api.model.racktivity.device.getFilterObject()
    if deviceguid:
        filterObj.add(view, 'guid', deviceguid)
    devices = p.api.model.racktivity.device.findAsView(filterObj, view)
    removekeys = ('viewguid','version')
    results = list()
    for device in devices:
        result = dict()
        for k in device.iterkeys():
            if k not in removekeys:
                result[k] = device[k]
        results.append(result)
    connectioninfo = dict()
    for device in results:
        deviceobject = p.api.model.racktivity.device.get(device['guid'])
        for powerport in deviceobject.powerports:
            if powerport.cableguid:
                filterObject = p.api.model.racktivity.meteringdevice.getFilterObject()
                filterObject.add('racktivity_view_meteringdevice_poweroutput', 'cableguid', powerport.cableguid)
                meteringdeviceguid = p.api.model.racktivity.meteringdevice.find(filterObject)[0]
                connectioninfo[powerport.sequence] = {'meteringdeviceguid': meteringdeviceguid, 'label': powerport.name}
            else:
                connectioninfo[powerport.sequence] = {'meteringdeviceguid': '', 'label': powerport.name}
        device['connectioninfo'] = connectioninfo
    return results

def errorcondition_list(errorconditionguid=""):
    view =  'racktivity_view_errorcondition_list'
    filterObj = p.api.model.racktivity.errorcondition.getFilterObject()
    if errorconditionguid:
        filterObj.add(view, 'errorconditionguid', errorconditionguid)
    errorconditions = p.api.model.racktivity.errorcondition.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for errorcondition in errorconditions:
        result = dict()
        for key in errorcondition.iterkeys():
            if key not in removekeys:
                result[key] = errorcondition[key]
        results.append(result)
    return results

def ipaddress_list(ipaddressguid=""):
    view =  'racktivity_view_ipaddress_list'
    filterObj = p.api.model.racktivity.ipaddress.getFilterObject()
    if ipaddressguid:
        filterObj.add(view, 'guid', ipaddressguid)
    ipaddresses = p.api.model.racktivity.ipaddress.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for ipaddress in ipaddresses:
        result = dict()
        for key in ipaddress.iterkeys():
            if key not in removekeys:
                result[key] = ipaddress[key]
        results.append(result)
    return results

def lan_list(backplaneguid="", languid=""):
    view =  'racktivity_view_lan_list'
    params={'backplaneguid':backplaneguid, 'guid':languid}
    filterObj = p.api.model.racktivity.lan.getFilterObject()
    for key,value in params.iteritems():
        if value:
            filterObj.add(view, key, value)
    lans = p.api.model.racktivity.lan.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for lan in lans:
        result = dict()
        for key in lan.iterkeys():
            if key != 'languid':
                result[key] = lan[key]
        results.append(result)
    return results

def location_list(locationguid=""):
    view =  'racktivity_view_location_list'
    filterObj = p.api.model.racktivity.location.getFilterObject()
    if locationguid:
        filterObj.add(view, 'guid', locationguid)
    locations = p.api.model.racktivity.location.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for location in locations:
        result = dict()
        for key in location.iterkeys():
            if key not in removekeys:
                result[key] = location[key]
        results.append(result)
    return results

def logicalview_list(name="", clouduserguid="", share="", tags=""):
    view =  'racktivity_view_logicalview_list'
    data = {"name":name, "clouduserguid":clouduserguid,"share":share, "tags":tags}
    filterObj = p.api.model.racktivity.logicalview.getFilterObject()
    for key in data:
        if data[key] != "":
            filterObj.add(view, key, data[key])
    logicalviews = p.api.model.racktivity.logicalview.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for logicalview in logicalviews:
        result = dict()
        for key in logicalview.iterkeys():
            if key not in removekeys:
                result[key] = logicalview[key]
        results.append(result)
    return results


def meteringdevice_list(meteringdevicetype="", rackguid="", parentmeteringdeviceguid=""):
    view = 'racktivity_view_meteringdevice_list'
    filters = ('meteringdevicetype', 'rackguid', 'parentmeteringdeviceguid')
    params={'meteringdevicetype':meteringdevicetype, 'rackguid':rackguid, 'parentmeteringdeviceguid': parentmeteringdeviceguid};
    filterobj = p.api.model.racktivity.meteringdevice.getFilterObject()
    for key, value in params.iteritems():
        if key in filters and value:
            filterobj.add(view, key, value)
    meteringdevices = p.api.model.racktivity.meteringdevice.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for meteringdevice in meteringdevices:
        result = dict()
        for key in meteringdevice.iterkeys():
            if key not in removekeys:
                result[key] = meteringdevice[key]
        results.append(result)
    return results

def meteringdeviceevent_list(meteringdeviceguid="", portsequence="", sensorsequence="", eventtype="", level="", thresholdguid="", latest=""):
    view =  'racktivity_view_meteringdeviceevent_list'
    params = {'meteringdeviceguid':meteringdeviceguid, 'portsequence':portsequence, 'sensorsequence':sensorsequence,
              'eventtype':eventtype, 'level':level, 'thresholdguid':thresholdguid, 'latest':latest}
    filterObj = p.api.model.racktivity.meteringdeviceevent.getFilterObject()
    filters = ('meteringdeviceguid', 'portsequence', 'sensorsequence', 'eventtype', 'level', 'thresholdguid', 'latest')
    for key, value in params.iteritems():
        if key in filters and value:
            filterObj.add(view, key, value)
    events = p.api.model.racktivity.meteringdeviceevent.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for event in events:
        result = dict()
        for key in event.iterkeys():
            if key not in removekeys:
                result[key] = event[key]
        results.append(result)
    return results

def monitoringinfo_list(monitoringinfoguid=""):
    view =  'racktivity_view_monitoringinfo_list'
    filterObj = p.api.model.racktivity.monitoringinfo.getFilterObject()
    if monitoringinfoguid:
        filterObj.add(view, 'guid', monitoringinfoguid)
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

def policy_list(policyguid="",name="", rootobjectaction="", rootobjecttype=""):
    filters = ('guid', 'name' ,'rootobjectaction','rootobjecttype')
    filterobj = p.api.model.racktivity.policy.getFilterObject()
    view = 'racktivity_view_policy_list'
    params={'guid':policyguid, 'name':name, 'rootobjectaction':rootobjectaction, 'rootobjecttype':rootobjecttype}
    for key, value in params.iteritems():
        if key in filters and value:
            filterobj.add(view, key, value)
    policies = p.api.model.racktivity.policy.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for policy in policies:
        result = dict()
        for key in policy.iterkeys():
            if key not in removekeys:
                result[key] = policy[key]
        results.append(result)
    return results

def resourcegroup_list(resourcegroupguid="",  customerguid="", deviceguid=""):
    params = {'guid': resourcegroupguid,
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
    view = defaultview
    for key, value in params.iteritems():
        if value:
            view = viewmap.get(key, defaultview)
            filterobj.add(view, key, value)
    results = p.api.model.racktivity.resourcegroup.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    for result in results:
        for key in removekeys:
            del result[key]
    return results

def rack_list(rackguid=""):
    view =  'racktivity_view_rack_list'
    filterobj = p.api.model.racktivity.rack.getFilterObject()
    if rackguid:
        filterobj.add(view, 'guid', rackguid)
    racks = p.api.model.racktivity.rack.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for rack in racks:
        result = dict()
        for key in rack.iterkeys():
            if key not in removekeys:
                result[key] = rack[key]
        results.append(result)
    return results

def room_list(roomguid=""):
    view = 'racktivity_view_room_list'
    filterobj = p.api.model.racktivity.room.getFilterObject()
    if roomguid:
        filterobj.add(view, 'guid', roomguid)
    rooms = p.api.model.racktivity.room.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for room in rooms:
        result = dict()
        for key in room.iterkeys():
            if key not in removekeys:
                result[key] = room[key]
        results.append(result)
    return results

def floor_list(floorguid=""):
    view = 'racktivity_view_floor_list'
    filterobj = p.api.model.racktivity.floor.getFilterObject()
    if floorguid:
        filterobj.add(view, 'guid', floorguid)
    floors = p.api.model.racktivity.floor.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for floor in floors:
        result = dict()
        for key in floor.iterkeys():
            if key not in removekeys:
                result[key] = floor[key]
        results.append(result)
    return results

def threshold_list(thresholdguid="", thresholdtype="",  thresholdimpacttype=""):
    view = 'racktivity_view_threshold_list'
    filterobj = p.api.model.racktivity.threshold.getFilterObject()
    filters=('thresholdguid', 'thresholdtype', 'thresholdimpacttype')
    params={'guid':thresholdguid, 'thresholdtype':thresholdtype, 'thresholdimpacttype':thresholdimpacttype}
    for key, value in params.iteritems():
        if key in filters and value:
            filterobj.add(view, key, value)
    thresholds = p.api.model.racktivity.threshold.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for threshold in thresholds:
        result = dict()
        for key in threshold.iterkeys():
            if key not in removekeys:
                result[key] = threshold[key]
        results.append(result)
    return results

def feed_list(feedguid="", datacenterguid="", feedproductiontype="", tags=""):
    view = 'racktivity_view_feed_list'
    filterobj = p.api.model.racktivity.feed.getFilterObject()
    params={'guid':feedguid, 'datacenterguid':datacenterguid, 'feedproductiontype':feedproductiontype, 'tags':tags}
    for key, value in params.iteritems():
        if value:
            filterobj.add(view, key, value)
    feeds = p.api.model.racktivity.feed.findAsView(filterobj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for feed in feeds:
        result = dict()
        for key in feed.iterkeys():
            if key not in removekeys:
                result[key] = feed[key]
        results.append(result)
    return results

def enterprise_list(name="", campus="", tags=""):
    defaultview =  'racktivity_view_enterprise_list'
    data = {"name":name, 'campus': campus, "tags":tags}
    viewmap = {'campus': 'racktivity_view_enterprise_campus'}
    filterObj = p.api.model.racktivity.enterprise.getFilterObject()
    for key, value in data.iteritems():
        if value:
            view = viewmap.get(key, defaultview)
            filterObj.add(view, key, data[key])
    
    enterprises = p.api.model.racktivity.enterprise.findAsView(filterObj, defaultview)
    removekeys = ('viewguid', 'version')
    results = list()
    for enterprise in enterprises:
        result = dict()
        for key in enterprise.iterkeys():
            if key not in removekeys:
                result[key] = enterprise[key]
        results.append(result)
    return results

def pod_list(podguid="", name="", alias="", room="", tags=""):
    view =  'racktivity_view_pod_list'
    data = {"guid": podguid, "name":name, "alias":alias, "room":room, "tags":tags}
    filterObj = p.api.model.racktivity.pod.getFilterObject()
    for key in data:
        if data[key] != "":
            filterObj.add(view, key, data[key])
    pods = p.api.model.racktivity.pod.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for pod in pods:
        result = dict()
        for key in pod.iterkeys():
            if key not in removekeys:
                result[key] = pod[key]
        results.append(result)
    return results

def row_list(rowguid="", name="", alias="", room="", pod="", tags=""):
    view =  'racktivity_view_row_list'
    data = {"guid": rowguid, "name":name, "alias":alias, "room":room, "pod":pod, "tags":tags}
    filterObj = p.api.model.racktivity.row.getFilterObject()
    for key in data:
        if data[key] != "":
            filterObj.add(view, key, data[key])
    rows = p.api.model.racktivity.row.findAsView(filterObj, view)
    removekeys = ('viewguid', 'version')
    results = list()
    for row in rows:
        result = dict()
        for key in row.iterkeys():
            if key not in removekeys:
                result[key] = row[key]
        results.append(result)
    return results

def autodiscoverysnmpmap_list(autodiscoverysnmpmapguid, manufacturer):
    view =  'racktivity_view_autodiscoverysnmpmap_list'
    filterObj = p.api.model.racktivity.autodiscoverysnmpmap.getFilterObject()
    if autodiscoverysnmpmapguid is not None:
        filterObj.add(view, 'guid', autodiscoverysnmpmapguid)
    if manufacturer is not None:
        filterObj.add(view, 'manufacturer', manufacturer)
    autodiscoverysnmpmaps = p.api.model.racktivity.autodiscoverysnmpmap.findAsView(filterObj, view)
    keys = ['guid','manufacturer']
    results = list()
    for autodiscoverysnmpmap in autodiscoverysnmpmaps:
        result = dict()
        for key in autodiscoverysnmpmap.iterkeys():
            if key in keys:
                if key == 'guid':
                    result['autodiscoverysnmpmapguid'] = autodiscoverysnmpmap['guid']
                else:
                    result[key] = autodiscoverysnmpmap[key]
        results.append(result)
    return results
