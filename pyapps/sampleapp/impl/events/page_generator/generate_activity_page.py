def main(q, i, p, params, tags):
    guid = params["eventBody"]
    key = params["eventKey"]
    template = """
    # Activity details
    *Name:* %(name)s
    *Description:* %(description)s
    *Location:* %(location)s
    *Start time:* %(starttime)s
    *End time:* %(endtime)s        
    *Type:* %(type)s
    *Status:* %(status)s    
    """
    activity = p.api.action.crm.activity.getObject(guid)
    searchresult = p.api.action.ui.page.find(name="activity_detail_%s"%guid)['result']
    parentpage = p.api.action.ui.page.find(name="Home", space="crm")['result'][0]
    if searchresult:
        p.api.action.ui.page.update(guid, "activity_detail_%s"%guid, "crm", "activity", parentpage, "crm activity", 
                                template%{"name": activity.name, "description": activity.description, "location": activity.location,
                                          "starttime": activity.starttime, "endtime": activity.endtime, "type": activity.type, 
                                          "status": activity.status})
    else:
        p.api.action.ui.page.create("activity_detail_%s"%guid, "crm", "activity", parentpage, "crm activity", 
                                template%{"name": activity.name, "description": activity.description, "location": activity.location,
                                          "starttime": activity.starttime, "endtime": activity.endtime, "type": activity.type, 
                                          "status": activity.status})
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.activity'