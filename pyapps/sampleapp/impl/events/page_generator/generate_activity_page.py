import urllib
import json
    
def main(q, i, p, params, tags):
    guid = params["eventBody"]
    key = params["eventKey"]
    template = """
# Activity details

* __Name:__ %(name)s
* __Description:__ %(description)s
* __Location:__ %(location)s
* __Start time:__ %(starttime)s
* __End time:__ %(endtime)s
* __Type:__ %(type)s
* __Status:__ %(status)s
<br />
<br />
[[wizard:title=Edit, name=activity_edit, extra=%(params)s]][[/wizard]]
[[wizard:title=Delete, name=activity_delete, extra=%(params)s]][[/wizard]]
    """
    activity = p.api.action.crm.activity.getObject(guid)
    searchresult = p.api.action.ui.page.find(name="activity_detail_%s"%guid)['result']
    parentpage = p.api.action.ui.page.find(name="Home", space="crm")['result'][0]
    params_ = urllib.quote(json.dumps({'activityguid': activity.guid}))
    if searchresult:
        p.api.action.ui.page.update(searchresult[0], "activity_detail_%s"%guid, "crm", "activity", parentpage, "crm activity", 
                                template%{"name": activity.name, "description": activity.description, "location": activity.location,
                                          "starttime": activity.starttime, "endtime": activity.endtime, "type": activity.type, 
                                          "status": activity.status, "params": params_, })
    else:
        p.api.action.ui.page.create("activity_detail_%s"%guid, "crm", "activity", parentpage, "crm activity", 
                                template%{"name": activity.name, "description": activity.description, "location": activity.location,
                                          "starttime": activity.starttime, "endtime": activity.endtime, "type": activity.type, 
                                          "status": activity.status, "params": params_, })
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.activity'
