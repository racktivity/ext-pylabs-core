import json

def main(q, i, p, params, tags):
    guid = params["eventBody"]
    key = params["eventKey"]
    template = """
# Group details
* __Name:__ %(name)s
* __Permissions:__ %(permissions)s
[[wizard:title=Edit, name=group_edit, extra=%(wizard_params)s]][[/wizard]]
[[wizard:title=Delete, name=group_delete, extra=%(wizard_params)s]][[/wizard]]

    """
    try:
        group = p.api.action.crm.group.getObject(guid)
    except:
        q.logger.log("Error getting group with guid %s"% guid , 7)
    
    
    wizard_params = json.dumps({'groupguid': group.guid})
    q.logger.log("search view for group %s"%guid,level=3) 
    searchresult = p.api.action.ui.page.find(name="group_detail_%s"%guid)['result']
    q.logger.log("search returned view %s"%str(searchresult),level=3)
    parentpage = p.api.action.ui.page.find(name="GroupOverview", space="crm")['result'][0]
    
    templateParams= dict()
    templateParams['wizard_params'] = wizard_params
    templateParams['groupguid'] = guid
    templateParams['name']=group.name
    templateParams['permissions']=group.permissions
    
    content = template% templateParams 
    
    if searchresult:
        p.api.action.ui.page.update(searchresult[0], "group_detail_%s"%guid, "crm", "group", parentpage, "crm group",content)
    else:
        p.api.action.ui.page.create("group_detail_%s"%guid, "crm", "group", parentpage, "crm group",content)        
        
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.store.crm.group'
