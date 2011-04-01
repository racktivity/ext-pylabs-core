__author__ = 'incubaid'

FIELDS = (
        'activityguid',
        'customerguid',
        'leadguid',
        'name',
        'type',
        'status',
        'priority'
        )
TYPE = "activity"
GUID_FIELD = "%sguid" % TYPE
DOMAIN = "crm"
VIEW = "%s_view_%s_list" % (DOMAIN, TYPE)

def get_model_handle(p):
    return p.api.model.crm.lead

def main(q, i, p, params, tags):
    handle = get_model_handle()
    f = handle.getFilterObject()

    for field in FIELDS:
        if field not in params:
            q.logger.log("Field %s not in params dict: not searching for field %s" % (field, field), 7)
            continue

        value = params[field]
        if value is None:
            q.logger.log("Field %s is None: not searching for field %s" % (field, field), 7)
            continue

        q.logger.log("Adding filter on field %s with value value %s" % (field, value), 7)
        f.add(VIEW, field, value)

    result = handle.find(f)
    params['result'] = result
    
    
    
    filterObject = p.api.model.crm.activity.getFilterObject()
    for key in params.iterkeys():
        if key == "activityguid" and params["activityguid"]:
            filterObject.add("crm_view_activity_list", "activityguid", params["activityguid"])
        if key == "customerguid" and params["customerguid"]:
            filterObject.add("crm_view_activity_list", "customerguid", params["customerguid"])
        if key == "leadguid" and params["leadguid"]:
            filterObject.add("crm_view_activity_list", "leadguid", params["leadguid"])
        if key == "name" and params["name"]:
            filterObject.add("crm_view_activity_list", "name", params["name"])
        if key == "type" and params["type"]:
            filterObject.add("crm_view_activity_list", "type", params["type"])
        if key == "status" and params["status"]:
            filterObject.add("crm_view_activity_list", "status", params["status"])
        if key == "priority" and params["priority"]:
            filterObject.add("crm_view_activity_list", "priority", params["priority"])
        
    result = p.api.model.crm.activity.find(filterObject)
    params["result"] = result