__author__ = 'incubaid'
__tags__ = 'activity', 'find'
__priority__ = 3

def main(q, i, p, params, tags):
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