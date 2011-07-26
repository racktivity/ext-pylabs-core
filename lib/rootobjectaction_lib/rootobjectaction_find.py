from pylabs import q,p

SPECIAL_VIEWS = {
    "device":{"macaddress": "racktivity_view_device_nicports", "cableguid":  "racktivity_view_device_powerports"},
    "meteringdevice": {"cableguid": "racktivity_view_meteringdevice_poweroutput"},
    "resourcegroup":  {"device": "racktivity_view_resourcegroup_device"},
    "feed": {"cableguid": "racktivity_view_feed_feedconnectors"},
    "enterprise" : {'campus': 'racktivity_view_enterprise_campus'},
    "pod" : {'rack': 'racktivity_view_pod_rack'},
    "row" : {'rack': 'racktivity_view_row_rack'}
}

def exists(view, obj, key, value):
    """
    This function determine if the "value" of the attribute "key" in onject "obj" exists or not
    Usually used to prevent creation of two objects with the same name
    sample usage: exists('racktivity_view_location_list', p.api.model.racktivity.location, "name", params['name'])
    """
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def find(rootobjectName, **params):
    model = getattr(p.api.model.racktivity, rootobjectName)
    defaultView = 'racktivity_view_%s_list'%rootobjectName
    specialViews = SPECIAL_VIEWS[rootobjectName] if rootobjectName in SPECIAL_VIEWS else None
    filterObject = model.getFilterObject()
    for param in params.iterkeys():
        if params[param] is None:
            continue
        if specialViews and param in specialViews:
            filterObject.add(specialViews[param], param , params[param])
        else:
            filterObject.add(defaultView, param , params[param])
    result = model.find(filterObject)
    return result

import functools
acl_find = functools.partial(find, "acl")
application_find = functools.partial(find, "application")
backplane_find =  functools.partial(find, "backplane")
cable_find = functools.partial(find, "cable")
clouduser_find = functools.partial(find, "clouduser")
cloudusergroup_find = functools.partial(find, "cloudusergroup")
customer_find = functools.partial(find, "customer")
datacenter_find = functools.partial(find, "datacenter")
device_find = functools.partial(find, "device")
errorcondition_find = functools.partial(find, "errorcondition")
ipaddress_find = functools.partial(find, "ipaddress")
lan_find = functools.partial(find, "lan")
location_find = functools.partial(find, "location")
logicalview_find = functools.partial(find, "logicalview")
meteringdeviceevent_find = functools.partial(find, "meteringdeviceevent")
monitoringinfo_find = functools.partial(find, "monitoringinfo")
policy_find = functools.partial(find, "policy")
resourcegroup_find = functools.partial(find, "resourcegroup")
rack_find = functools.partial(find, "rack")
room_find = functools.partial(find, "room")
floor_find = functools.partial(find, "floor")
feed_find = functools.partial(find, "feed")
enterprise_find = functools.partial(find, "enterprise")
pod_find = functools.partial(find, "pod")
row_find = functools.partial(find, "row")
autodiscoverysnmpmap_find = functools.partial(find, "autodiscoverysnmpmap")


def job_find(actionname=None, deviceguid =None, agentguid="",applicationguid="",datacenterguid="",fromTime="",toTime="",clouduserguid=""):
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
